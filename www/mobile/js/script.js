$(function() {
	
	var log = function(msg) {
		if (console) {
			console.log(msg);
		}
	};
	
	var settings = {
		refreshInterval: 30 * 1000, // 30 seconds
		useLocalCache: true
	};
	
	/*
	 * utility objects
	 */
	
	var DAYS = [
		'Sunday','Monday','Tuesday','Wednesday',
		'Thursday','Friday','Saturday'
	];
	var MONTHS = [
		'January','February','March','April','May',
		'June','July','August','September','October',
		'November','December'
	];

	var formatDate = function(s) {

		var year = parseInt(s.substr(0, 4), 10);
		var month = parseInt(s.substr(5, 2), 10);
		var day = parseInt(s.substr(8, 2), 10);
		
		var dt = new Date(year, month - 1, day);
		
		var d = DAYS[dt.getDay()];
		var m = MONTHS[dt.getMonth()];
		
		return d + " " + m + " " + day + ", " + year;

	};
	
	var formatTime = function(s) {
		
		var hour = parseInt(s.substr(0, 2), 10);
		var minute = s.substr(3, 2);
		var ampm = hour > 11 ? "pm" : "am";
		
		if (hour === 0) {
			hour = 12;
		} else if (hour > 12) {
			hour -= 12;
		}
		
		return hour + ":" + minute + ampm;
		
	};
	
	var getSessions = function(callback, qs) {
		var url = '/api/sessions/';
		if (qs !== undefined) {
			url += "?" + qs;
		}
		$.getJSON(url, function(data) {
			var sessions = {};
			_.each(data.objects, function(o) {
				if (sessions[o.date] === undefined) {
					sessions[o.date] = {};
				}
				if (sessions[o.date][o.start_time] === undefined) {
					sessions[o.date][o.start_time] = [];
				}
				sessions[o.date][o.start_time].push(o);
			});
			var days = [];
			_.each(sessions, function(v, k) {
				var day = {date: k, dateStr: formatDate(k), slots: []};
				_.each(v, function(v, k) {
					var slot = {time: k, timeStr: formatTime(k), sessions: v};
					day.slots.push(slot);
				});
				days.push(day);
			});
			callback(days);
		});
	};
	
	var IncrementalCollection = Backbone.Collection.extend({
		
		newCount: 0,
		
		refresh : function(models, options) {
			
			models = models || [];
			options = options || {};
			
			if (this.length === 0) {
				
				_.each(models, function(m) {
					m.isNew = false;
				});
				
				this.add(models, {silent: true});
				
			} else {
				
				var localIds = this.pluck("id");
				var remoteIds = _.pluck(models, "id");
				
				this.newCount = 0;
				
				this.each(function(m) {
					m.set({isNew: false});
				});
				
				_.each(this.reject(function(m) {
					return _.include(remoteIds, m.id);
				}), function(m) {
					this.remove(m);
					if (m.view) {
						m.view.remove();
					}
				}, this);
				
				_(models).chain()
					.reject(function(m) { return _.include(localIds, m.id); })
					.sortBy(function(m) { return parseInt(m.id, 10); })
					.each(function(m) { this.add(m, {silent: true}); this.newCount++; }, this)
					.value();
				
			}
			
			if (!options.silent) { this.trigger('refresh', this, options); }
			return this;
			
		}
		
	});

	var ListModel = Backbone.Model.extend({
		clear: function() {
			this.destroy();
			this.view.remove();
		}
	});
	
	/*
	 * basic scripty stuff
	 */
	
	var $nav = $('a.nav');
	$nav.click(function(ev) {
		$nav.removeClass('active');
		if (this.href !== '#') {
			$(this).addClass('active');
		}
	});
	
	/*
	 * model and list for TCampDC twitter updates
	 */
	
	var Update = ListModel.extend({
		defaults: { isNew: true }
	});

	var UpdateList = IncrementalCollection.extend({

		model: Update,
		url: '/api/updates/',

		comparator: function(update) {
			return -parseInt(update.get("id"), 10);
		},
		parse: function(response) {
			return response.objects;
		}

	});
	
	var Updates = new UpdateList();
	
	/*
	 * model and list for other social feed items
	 */
	
	var SocialItem = ListModel.extend({
		defaults: { isNew: true }
	});
	
	var SocialCollection = IncrementalCollection.extend({
		
		model: SocialItem,
		url: '/api/socialfeed/',
		
		comparator: function(update) {
			return -parseInt(update.get("id"), 10);
		},
		parse: function(response) {
			return response.objects;
		}
		
	});
	
	var SocialFeed = new SocialCollection();
	
	/*
	 * views
	 */

	var SocialView = Backbone.View.extend({

		tagName: "li",
		template: _.template($('#template-social').html()),

		initialize: function() {
			_.bindAll(this, 'render');
			this.model.bind('change', this.render);
			this.model.view = this;
		},

		render: function() {
			var $el = $(this.el);
			$el.html(this.template(this.model.toJSON()));
			if (this.model.get('isNew')) {
				$el.addClass('new');
			} else {
				$el.removeClass('new');
			}
			return this;
		},

		remove: function() {
			$(this.el).remove();
		},

		clear: function() {
			this.model.clear();
		}

	});
	
	var UpdateView = Backbone.View.extend({

		tagName: "li",
		template: _.template($('#template-update').html()),

		initialize: function() {
			_.bindAll(this, 'render');
			this.model.bind('change', this.render);
			this.model.view = this;
		},

		render: function() {
			var $el = $(this.el);
			$el.html(this.template(this.model.toJSON()));
			if (this.model.get('isNew')) {
				$el.addClass('new');
			} else {
				$el.removeClass('new');
			}
			return this;
		},

		remove: function() {
			$(this.el).remove();
		},

		clear: function() {
			this.model.clear();
		}

	});
	
	// main app view
	
	var AppView = Backbone.View.extend({
		
		el: $('#main'),
		
		initialize: function() {
			Updates.bind('refresh', this.loadUpdates);
			SocialFeed.bind('refresh', this.loadSocialFeed);
		},
		
		loadUpdates: function() {
			Updates.each(function(update) {
				var view = update.view || new UpdateView({model: update});
				this.$('ul.updates').append(view.render().el);
			});
		},
		
		loadSocialFeed: function() {
			SocialFeed.each(function(item){
				var view = item.view || new SocialView({model: item});
				this.$('ul.social').append(view.render().el);
			});
		}
		
	});
	
	window.App = new AppView();
	
	/*
	 * controller for main application
	 */
	
	var TransparencyCamp = Backbone.Controller.extend({
		
		routes: {
			"":         "dashboard",
			"updates":  "updates", 
			"sessions": "sessions",
			"venue":    "venue",
			"social":   "social"
		},
		
		currentPanel: null,
		intervals: [],
		sessionsTemplate: _.template($('#template-sessions').html()),
		
		showPanel: function(id) {
			_.each(this.intervals, function(i) { clearInterval(i); });
			$('div.panel').hide().filter('#panel-' + id).show();
			this.currentPanel = id;
		},
		
		dashboard: function() {
			
			var that = this;
			
			this.showPanel('dashboard');
			
			$.getJSON('/api/photos/?limit=4', function(data) {
				var $photos = $('p.flickr a');
				_.each(data.objects, function(p, index) {
					$($photos[index])
						.attr('href', p.url)
						.find('img')
						.attr('src', p.url_square);
				});
			});
			
			getSessions(function(data) {
				if (data.length > 0) {
					data[0].dateStr = 'Coming up next...';
					$('#panel-dashboard div.next-sessions').html(
						that.sessionsTemplate({sessions: data})
					);
				}
			}, 'next');
			
			log('route dashboard');
			
		},
		
		updates: function() {
			
			var fetch = function() {
				Updates.fetch({success: function(collection, resp) {
					if (settings.useLocalCache) {
						log('storing updates in cache');
						store.set('updates-data', collection.toJSON());
					}
				}});
			};
			
			if (settings.useLocalCache) {
				var cachedData = store.get('updates-data');
				if (cachedData) {
					log('loading updates from cache');
					Updates.refresh(cachedData);
				}
			}
			this.showPanel('updates');
			log('fetching updates from server');
			
			fetch();
			
			this.intervals.push(setInterval(fetch, settings.refreshInterval));
			
		},
		
		sessions: function() {
			
			var that = this;
			
			if (settings.useLocalCache) {
				var cachedData = store.get('sessions-data');
				if (cachedData) {
					log('loading sessions from cache');
					$('.sessions-container').html(that.sessionsTemplate({sessions: cachedData}));
				}
			}
			this.showPanel('sessions');
			log('fetching sessions from server');
			
			getSessions(function(data) {
				$('.sessions-container').html(that.sessionsTemplate({sessions: data}));
				store.set('sessions-data', data);
			}, 'latertoday');
			
			log('route sessions');
			
		},
		
		venue: function() {
			this.showPanel('venue');
			log('route venue');
		},
		
		social: function() {
			
			var fetch = function() {
				SocialFeed.fetch({success: function(collection, resp) {
					if (settings.useLocalCache) {
						log('storing updates in cache');
						store.set('social-data', collection.toJSON());
					}
				}});
			};
			
			if (settings.useLocalCache) {
				var cachedData = store.get('social-data');
				if (cachedData) {
					log('loading social from cache');
					SocialFeed.refresh(cachedData);
				}
			}
			this.showPanel('social');
			log('fetching social from server');
			
			fetch();
			
			this.intervals.push(setInterval(fetch, settings.refreshInterval));
			
		}
		
	});
	
	var controller = new TransparencyCamp();
	Backbone.history.start();
	
	if (applicationCache) {
		applicationCache.addEventListener('updateready', function() {
			if (confirm('An update is available. Reload now?')) {
				window.location.reload();
			}
		});
	}
	
	//store.clear();
	
});