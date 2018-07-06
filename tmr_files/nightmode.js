function StorageSupported(){try{localStorage.setItem("testkey","testvalue");localStorage.removeItem("testkey");return true;}catch(e){return false;}}
function nightModeOn(){jQuery('html').addClass('nightmode');localStorage.setItem('nightmode','y');}
function nightModeOff(){jQuery('html').removeClass('nightmode');localStorage.removeItem('nightmode');}
function isUrlBlacklisted(){var path=window.location.pathname;var blackListedUrls=["/wp-admin","/wp-login"];for(var i=0;i<blackListedUrls.length;i++){if(path.startsWith(blackListedUrls[i])){return true;}}
return false;}
if(StorageSupported()&&!isUrlBlacklisted()){if(localStorage.getItem('nightmode')!==null){jQuery('html').addClass('nightmode');}
if(localStorage.getItem('fontscale')!==null){resizeText(parseFloat(localStorage.getItem('fontscale'),false));}}
function resizeText(multiplier,storage){jQuery('#main article .entry-content p span').css('font-size','');if(jQuery('#main article .entry-content p').css('font-size')==""){jQuery('#main article .entry-content p').css('font-size','1.0em');}
jQuery('#main article .entry-content p').css('font-size',parseFloat(jQuery('#main article .entry-content p').css('font-size'))+(multiplier*2)+"px");if(storage&&StorageSupported()){var offset=multiplier;if(localStorage.getItem('fontscale')!==null){offset=offset+parseFloat(localStorage.getItem('fontscale'));}
localStorage.setItem('fontscale',offset);}}