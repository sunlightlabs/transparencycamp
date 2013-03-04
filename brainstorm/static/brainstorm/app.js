(function(window, $, undefined){

// jQuery form
$.fn.ajaxSubmit || (function(c){function n(a){var e=a.data;a.isDefaultPrevented()||(a.preventDefault(),c(this).ajaxSubmit(e))}function v(a){var e=a.target,g=c(e);if(!g.is("[type=submit],[type=image]")){e=g.closest("[type=submit]");if(0===e.length)return;e=e[0]}var b=this;b.clk=e;"image"==e.type&&(void 0!==a.offsetX?(b.clk_x=a.offsetX,b.clk_y=a.offsetY):"function"==typeof c.fn.offset?(g=g.offset(),b.clk_x=a.pageX-g.left,b.clk_y=a.pageY-g.top):(b.clk_x=a.pageX-e.offsetLeft,b.clk_y=a.pageY-e.offsetTop));setTimeout(function(){b.clk=
b.clk_x=b.clk_y=null},100)}function r(){if(c.fn.ajaxSubmit.debug){var a="[jquery.form] "+Array.prototype.join.call(arguments,"");window.console&&window.console.log?window.console.log(a):window.opera&&window.opera.postError&&window.opera.postError(a)}}var A,D;A=void 0!==c("<input type='file'/>").get(0).files;D=void 0!==window.FormData;c.fn.ajaxSubmit=function(a){function e(b){function e(){function a(){try{var b=(p.contentWindow?p.contentWindow.document:p.contentDocument?p.contentDocument:p.document).readyState;
r("state = "+b);b&&"uninitialized"==b.toLowerCase()&&setTimeout(a,50)}catch(c){r("Server abort: ",c," (",c.name,")"),f(B),u&&clearTimeout(u),u=void 0}}var b=l.attr("target"),h=l.attr("action");j.setAttribute("target",n);g||j.setAttribute("method","POST");h!=d.url&&j.setAttribute("action",d.url);!d.skipEncodingOverride&&(!g||/post/i.test(g))&&l.attr({encoding:"multipart/form-data",enctype:"multipart/form-data"});d.timeout&&(u=setTimeout(function(){v=!0;f(z)},d.timeout));var m=[];try{if(d.extraData)for(var k in d.extraData)d.extraData.hasOwnProperty(k)&&
(c.isPlainObject(d.extraData[k])&&d.extraData[k].hasOwnProperty("name")&&d.extraData[k].hasOwnProperty("value")?m.push(c('<input type="hidden" name="'+d.extraData[k].name+'">').val(d.extraData[k].value).appendTo(j)[0]):m.push(c('<input type="hidden" name="'+k+'">').val(d.extraData[k]).appendTo(j)[0]));d.iframeTarget||(w.appendTo("body"),p.attachEvent?p.attachEvent("onload",f):p.addEventListener("load",f,!1));setTimeout(a,15);document.createElement("form").submit.apply(j)}finally{j.setAttribute("action",
h),b?j.setAttribute("target",b):l.removeAttr("target"),c(m).remove()}}function f(a){if(!h.aborted&&!C){try{s=p.contentWindow?p.contentWindow.document:p.contentDocument?p.contentDocument:p.document}catch(b){r("cannot access response document: ",b),a=B}if(a===z&&h)h.abort("timeout"),x.reject(h,"timeout");else if(a==B&&h)h.abort("server abort"),x.reject(h,"error","server abort");else if(s&&s.location.href!=d.iframeSrc||v){p.detachEvent?p.detachEvent("onload",f):p.removeEventListener("load",f,!1);a="success";
var e;try{if(v)throw"timeout";var g="xml"==d.dataType||s.XMLDocument||c.isXMLDoc(s);r("isXml="+g);if(!g&&(window.opera&&(null===s.body||!s.body.innerHTML))&&--D){r("requeing onLoad callback, DOM not available");setTimeout(f,250);return}var j=s.body?s.body:s.documentElement;h.responseText=j?j.innerHTML:null;h.responseXML=s.XMLDocument?s.XMLDocument:s;g&&(d.dataType="xml");h.getResponseHeader=function(a){return{"content-type":d.dataType}[a]};j&&(h.status=Number(j.getAttribute("status"))||h.status,h.statusText=
j.getAttribute("statusText")||h.statusText);var k=(d.dataType||"").toLowerCase(),l=/(json|script|text)/.test(k);if(l||d.textarea){var q=s.getElementsByTagName("textarea")[0];if(q)h.responseText=q.value,h.status=Number(q.getAttribute("status"))||h.status,h.statusText=q.getAttribute("statusText")||h.statusText;else if(l){var n=s.getElementsByTagName("pre")[0],E=s.getElementsByTagName("body")[0];n?h.responseText=n.textContent?n.textContent:n.innerText:E&&(h.responseText=E.textContent?E.textContent:E.innerText)}}else"xml"==
k&&(!h.responseXML&&h.responseText)&&(h.responseXML=H(h.responseText));try{var g=h,j=d,t=g.getResponseHeader("content-type")||"",F="xml"===k||!k&&0<=t.indexOf("xml"),y=F?g.responseXML:g.responseText;F&&"parsererror"===y.documentElement.nodeName&&c.error&&c.error("parsererror");j&&j.dataFilter&&(y=j.dataFilter(y,k));"string"===typeof y&&("json"===k||!k&&0<=t.indexOf("json")?y=I(y):("script"===k||!k&&0<=t.indexOf("javascript"))&&c.globalEval(y));A=y}catch(J){a="parsererror",h.error=e=J||a}}catch(G){r("error caught: ",
G),a="error",h.error=e=G||a}h.aborted&&(r("upload aborted"),a=null);h.status&&(a=200<=h.status&&300>h.status||304===h.status?"success":"error");"success"===a?(d.success&&d.success.call(d.context,A,"success",h),x.resolve(h.responseText,"success",h),m&&c.event.trigger("ajaxSuccess",[h,d])):a&&(void 0===e&&(e=h.statusText),d.error&&d.error.call(d.context,h,a,e),x.reject(h,"error",e),m&&c.event.trigger("ajaxError",[h,d,e]));m&&c.event.trigger("ajaxComplete",[h,d]);m&&!--c.active&&c.event.trigger("ajaxStop");
d.complete&&d.complete.call(d.context,h,a);C=!0;d.timeout&&clearTimeout(u);setTimeout(function(){d.iframeTarget||w.remove();h.responseXML=null},100)}}}var j=l[0],k,d,m,n,w,p,h,t,v,u;t=!!c.fn.prop;var x=c.Deferred();if(b)for(k=0;k<q.length;k++)b=c(q[k]),t?b.prop("disabled",!1):b.removeAttr("disabled");d=c.extend(!0,{},c.ajaxSettings,a);d.context=d.context||d;n="jqFormIO"+(new Date).getTime();d.iframeTarget?(w=c(d.iframeTarget),(b=w.attr("name"))?n=b:w.attr("name",n)):(w=c('<iframe name="'+n+'" src="'+
d.iframeSrc+'" />'),w.css({position:"absolute",top:"-1000px",left:"-1000px"}));p=w[0];h={aborted:0,responseText:null,responseXML:null,status:0,statusText:"n/a",getAllResponseHeaders:function(){},getResponseHeader:function(){},setRequestHeader:function(){},abort:function(a){var b="timeout"===a?"timeout":"aborted";r("aborting upload... "+b);this.aborted=1;try{p.contentWindow.document.execCommand&&p.contentWindow.document.execCommand("Stop")}catch(e){}w.attr("src",d.iframeSrc);h.error=b;d.error&&d.error.call(d.context,
h,b,a);m&&c.event.trigger("ajaxError",[h,d,b]);d.complete&&d.complete.call(d.context,h,b)}};(m=d.global)&&0===c.active++&&c.event.trigger("ajaxStart");m&&c.event.trigger("ajaxSend",[h,d]);if(d.beforeSend&&!1===d.beforeSend.call(d.context,h,d))return d.global&&c.active--,x.reject(),x;if(h.aborted)return x.reject(),x;if(t=j.clk)if((b=t.name)&&!t.disabled)d.extraData=d.extraData||{},d.extraData[b]=t.value,"image"==t.type&&(d.extraData[b+".x"]=j.clk_x,d.extraData[b+".y"]=j.clk_y);var z=1,B=2;t=c("meta[name=csrf-token]").attr("content");
if((b=c("meta[name=csrf-param]").attr("content"))&&t)d.extraData=d.extraData||{},d.extraData[b]=t;d.forceSync?e():setTimeout(e,10);var A,s,D=50,C,H=c.parseXML||function(a,b){window.ActiveXObject?(b=new ActiveXObject("Microsoft.XMLDOM"),b.async="false",b.loadXML(a)):b=(new DOMParser).parseFromString(a,"text/xml");return b&&b.documentElement&&"parsererror"!=b.documentElement.nodeName?b:null},I=c.parseJSON||function(a){return window.eval("("+a+")")};return x}if(!this.length)return r("ajaxSubmit: skipping submit process - no element selected"),
this;var g,b,l=this;"function"==typeof a&&(a={success:a});g=this.attr("method");b=this.attr("action");(b=(b="string"===typeof b?c.trim(b):"")||window.location.href||"")&&(b=(b.match(/^([^#]+)/)||[])[1]);a=c.extend(!0,{url:b,success:c.ajaxSettings.success,type:g||"GET",iframeSrc:/^https/i.test(window.location.href||"")?"javascript:false":"about:blank"},a);b={};this.trigger("form-pre-serialize",[this,a,b]);if(b.veto)return r("ajaxSubmit: submit vetoed via form-pre-serialize trigger"),this;if(a.beforeSerialize&&
!1===a.beforeSerialize(this,a))return r("ajaxSubmit: submit aborted via beforeSerialize callback"),this;var j=a.traditional;void 0===j&&(j=c.ajaxSettings.traditional);var q=[],f,m=this.formToArray(a.semantic,q);a.data&&(a.extraData=a.data,f=c.param(a.data,j));if(a.beforeSubmit&&!1===a.beforeSubmit(m,this,a))return r("ajaxSubmit: submit aborted via beforeSubmit callback"),this;this.trigger("form-submit-validate",[m,this,a,b]);if(b.veto)return r("ajaxSubmit: submit vetoed via form-submit-validate trigger"),
this;b=c.param(m,j);f&&(b=b?b+"&"+f:f);"GET"==a.type.toUpperCase()?(a.url+=(0<=a.url.indexOf("?")?"&":"?")+b,a.data=null):a.data=b;var k=[];a.resetForm&&k.push(function(){l.resetForm()});a.clearForm&&k.push(function(){l.clearForm(a.includeHidden)});if(!a.dataType&&a.target){var B=a.success||function(){};k.push(function(b){var e=a.replaceTarget?"replaceWith":"html";c(a.target)[e](b).each(B,arguments)})}else a.success&&k.push(a.success);a.success=function(b,c,e){for(var g=a.context||this,f=0,d=k.length;f<
d;f++)k[f].apply(g,[b,c,e||l,l])};f=0<c('input[type=file]:enabled[value!=""]',this).length;b="multipart/form-data"==l.attr("enctype")||"multipart/form-data"==l.attr("encoding");j=A&&D;r("fileAPI :"+j);var z;if(!1!==a.iframe&&(a.iframe||(f||b)&&!j))a.closeKeepAlive?c.get(a.closeKeepAlive,function(){z=e(m)}):z=e(m);else if((f||b)&&j){var n=new FormData;for(b=0;b<m.length;b++)n.append(m[b].name,m[b].value);if(a.extraData){b=c.param(a.extraData).split("&");j=b.length;f=[];var u,v;for(u=0;u<j;u++)b[u]=
b[u].replace(/\+/g," "),v=b[u].split("="),f.push([decodeURIComponent(v[0]),decodeURIComponent(v[1])]);for(b=0;b<f.length;b++)f[b]&&n.append(f[b][0],f[b][1])}a.data=null;f=c.extend(!0,{},c.ajaxSettings,a,{contentType:!1,processData:!1,cache:!1,type:g||"POST"});a.uploadProgress&&(f.xhr=function(){var b=jQuery.ajaxSettings.xhr();b.upload&&b.upload.addEventListener("progress",function(b){var c=0,e=b.loaded||b.position,f=b.total;b.lengthComputable&&(c=Math.ceil(100*(e/f)));a.uploadProgress(b,e,f,c)},!1);
return b});f.data=null;var C=f.beforeSend;f.beforeSend=function(a,b){b.data=n;C&&C.call(this,a,b)};z=c.ajax(f)}else z=c.ajax(a);l.removeData("jqxhr").data("jqxhr",z);for(f=0;f<q.length;f++)q[f]=null;this.trigger("form-submit-notify",[this,a]);return this};c.fn.ajaxForm=function(a){a=a||{};a.delegation=a.delegation&&c.isFunction(c.fn.on);if(!a.delegation&&0===this.length){var e=this.selector,g=this.context;if(!c.isReady&&e)return r("DOM not ready, queuing ajaxForm"),c(function(){c(e,g).ajaxForm(a)}),
this;r("terminating; zero elements found by selector"+(c.isReady?"":" (DOM not ready)"));return this}return a.delegation?(c(document).off("submit.form-plugin",this.selector,n).off("click.form-plugin",this.selector,v).on("submit.form-plugin",this.selector,a,n).on("click.form-plugin",this.selector,a,v),this):this.ajaxFormUnbind().bind("submit.form-plugin",a,n).bind("click.form-plugin",a,v)};c.fn.ajaxFormUnbind=function(){return this.unbind("submit.form-plugin click.form-plugin")};c.fn.formToArray=function(a,
e){var g=[];if(0===this.length)return g;var b=this[0],l=a?b.getElementsByTagName("*"):b.elements;if(!l)return g;var j,q,f,m,k,n;j=0;for(n=l.length;j<n;j++)if(k=l[j],f=k.name)if(a&&b.clk&&"image"==k.type)!k.disabled&&b.clk==k&&(g.push({name:f,value:c(k).val(),type:k.type}),g.push({name:f+".x",value:b.clk_x},{name:f+".y",value:b.clk_y}));else if((m=c.fieldValue(k,!0))&&m.constructor==Array){e&&e.push(k);q=0;for(k=m.length;q<k;q++)g.push({name:f,value:m[q]})}else if(A&&"file"==k.type&&!k.disabled)if(e&&
e.push(k),m=k.files,m.length)for(q=0;q<m.length;q++)g.push({name:f,value:m[q],type:k.type});else g.push({name:f,value:"",type:k.type});else null!==m&&"undefined"!=typeof m&&(e&&e.push(k),g.push({name:f,value:m,type:k.type,required:k.required}));if(!a&&b.clk&&(l=c(b.clk),j=l[0],(f=j.name)&&!j.disabled&&"image"==j.type))g.push({name:f,value:l.val()}),g.push({name:f+".x",value:b.clk_x},{name:f+".y",value:b.clk_y});return g};c.fn.formSerialize=function(a){return c.param(this.formToArray(a))};c.fn.fieldSerialize=
function(a){var e=[];this.each(function(){var g=this.name;if(g){var b=c.fieldValue(this,a);if(b&&b.constructor==Array)for(var l=0,j=b.length;l<j;l++)e.push({name:g,value:b[l]});else null!==b&&"undefined"!=typeof b&&e.push({name:this.name,value:b})}});return c.param(e)};c.fn.fieldValue=function(a){for(var e=[],g=0,b=this.length;g<b;g++){var l=c.fieldValue(this[g],a);null===l||("undefined"==typeof l||l.constructor==Array&&!l.length)||(l.constructor==Array?c.merge(e,l):e.push(l))}return e};c.fieldValue=
function(a,e){var g=a.name,b=a.type,l=a.tagName.toLowerCase();void 0===e&&(e=!0);if(e&&(!g||a.disabled||"reset"==b||"button"==b||("checkbox"==b||"radio"==b)&&!a.checked||("submit"==b||"image"==b)&&a.form&&a.form.clk!=a||"select"==l&&-1==a.selectedIndex))return null;if("select"==l){var j=a.selectedIndex;if(0>j)return null;for(var g=[],l=a.options,n=(b="select-one"==b)?j+1:l.length,j=b?j:0;j<n;j++){var f=l[j];if(f.selected){var m=f.value;m||(m=f.attributes&&f.attributes.value&&!f.attributes.value.specified?
f.text:f.value);if(b)return m;g.push(m)}}return g}return c(a).val()};c.fn.clearForm=function(a){return this.each(function(){c("input,select,textarea",this).clearFields(a)})};c.fn.clearFields=c.fn.clearInputs=function(a){var e=/^(?:color|date|datetime|email|month|number|password|range|search|tel|text|time|url|week)$/i;return this.each(function(){var g=this.type,b=this.tagName.toLowerCase();if(e.test(g)||"textarea"==b)this.value="";else if("checkbox"==g||"radio"==g)this.checked=!1;else if("select"==
b)this.selectedIndex=-1;else if("file"==g)/MSIE/.test(navigator.userAgent)?c(this).replaceWith(c(this).clone()):c(this).val("");else if(a&&(!0===a&&/hidden/.test(g)||"string"==typeof a&&c(this).is(a)))this.value=""})};c.fn.resetForm=function(){return this.each(function(){("function"==typeof this.reset||"object"==typeof this.reset&&!this.reset.nodeType)&&this.reset()})};c.fn.enable=function(a){void 0===a&&(a=!0);return this.each(function(){this.disabled=!a})};c.fn.selected=function(a){void 0===a&&
(a=!0);return this.each(function(){var e=this.type;"checkbox"==e||"radio"==e?this.checked=a:"option"==this.tagName.toLowerCase()&&(e=c(this).parent("select"),a&&(e[0]&&"select-one"==e[0].type)&&e.find("option").selected(!1),this.selected=a)})};c.fn.ajaxSubmit.debug=!1})(jQuery);

// monkeypatch $.on, $.off for old versions of jQuery
$.fn.on || (
  $.fn.on = function(e, sel, cb){
    if(typeof sel == 'function'){
      cb = sel;
      $(this).live(e, cb);
    }else{
      $(this).delegate(sel, e, cb);
    }
    return $(this);
  }
);
$.fn.off || (
  $.fn.off = function(e, sel){
    if(!sel){
      $(this).die(e);
    }else{
      $(this).undelegate(sel, e);
    }
    return $(this);
  }
);

// bind at domready
$(function(){

  $(window).on('submit', '.brainstorm-votable form, .brainstorm-voted form', function(e){
    e.preventDefault();
    e.stopPropagation();
    var el = $(this),
        target = '#' + el.parents('.brainstorm-item').attr('id');

    el.ajaxSubmit({
      target: target,
      replaceTarget: true,
      success: function(){
        $(window).trigger('repaint.brainstorm', {elem: target});
      }
    });

  });

});

})(this, window.jQuery || window.zepto);