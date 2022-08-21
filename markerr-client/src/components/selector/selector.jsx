import { h, Fragment } from "preact";
import { useEffect } from "preact/hooks";
import "theroomjs/dist/theroom.min.js";
import { finder } from "@medv/finder";
import { SipLineIcon } from "../icons";
import { createXpath } from "../../annotator/utils";

const Selector = (props) => {
	const { setPopupOpen, setElements } = props;

	useEffect(() => {
		// whenever elements changes, this rerenders
		// console.log("rendered")
		if (theRoom) {
			window.theRoom.on("click", function (element, event) {
				let cssSelector = finder(element);
				let xpath = createXpath(element);
				// remove classname added by theroom
				// xpath = xpath.replace('[@class=" theRoom"	]', "");
				element.cssSelector = cssSelector;
				element.xpath = xpath;
				setElements((elements) => [
					...elements,
					{
						element: element,
						rId: elements.length + 1,
                        cssSelector: cssSelector,
                        xpath: xpath
					},
				]);
				window.theRoom.stop(true);
			});
		}
	}, []);

	const startInspector = () => {
		window.theRoom.start();
		setPopupOpen(false);
	};

	return (
		<button
			id="annotator-inspector-button"
			className="reset"
			onClick={startInspector}
			title="Pick an HTML element"
		>
			<SipLineIcon id="annotator-inspector-button-icon" className="icon-sm" />
		</button>
	);
};


export default Selector;