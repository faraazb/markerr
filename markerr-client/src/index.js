import habitat from "preact-habitat";
import "./style/reset.css";
import "./style/index.css";
import "./style/theme.css";
import "./style/buttons.css";
import {Annotator} from "./annotator/annotator";


console.debug('Markerr script loaded!');

let _habitat = habitat(Annotator);

_habitat.render({
  selector: '[data-widget-host="habitat"]',
  clean: true
});


// Create a div for the HTML element inspector (theroom.js)
if (window.attachEvent) {
    window.attachEvent('onload', inject);
} else {
    window.addEventListener('load', inject, false);
}

function inject() {
    let inspector = document.createElement('div');
    inspector.id = 'annotator-inspector';
    inspector.className = 'annotator-element-inspector';
    document.body.appendChild(inspector);
}
