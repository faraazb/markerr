import { h, Fragment } from "preact";
import "theroomjs/dist/theroom.min.js";
import { finder } from "@medv/finder";
import { MarkerIcon } from "../icons";
import { createXpath } from "../../annotator/utils";

const Highlighter = (props) => {
	const { setElements } = props;

	const startHighlighter = () => {
		// console.log("getting highlighted stuff");
		const selection = window.getSelection();
		if (!selection.rangeCount) return;
        const selectedText = selection.toString();

		const selectionRange = selection.getRangeAt(0);
		// console.log("Selected elements:");
		let highlightContainers = [];

		let ranges = selectionRange.cloneContents().querySelectorAll("*");
		if (ranges.length > 0) {
			ranges.forEach((element) => {
				// to get the ref to the actual HTMl el, I need the CSS selector anyway
				//  so don't delay find the selector till POSTing comments
				let cssSelector = finder(element);
				let xpath = createXpath(element);
				// console.log(cssSelector, xpath);
				const refToElement = document.querySelectorAll(cssSelector)[0];
				refToElement.cssSelector = cssSelector;
				refToElement.xpath = xpath;
				// console.log(refToElement);
				highlightContainers.push({
					el: refToElement,
					text: element.innerText,
                    cssSelector: cssSelector,
                    xpath: xpath
				});
			});
		} else {
			let element = selectionRange.commonAncestorContainer.parentElement;
			let cssSelector = finder(element);
			let xpath = createXpath(element);
			element.cssSelector = cssSelector;
			element.xpath = xpath;
			highlightContainers.push({
				el: element,
				text: selectedText,
                cssSelector: cssSelector,
                xpath: xpath
			});
		}

		// highlight is the entire text selection, element can have multiple nodes 
        // with their own selection texts
		setElements((elements) => [
			...elements,
			{
				rId: elements.length + 1,
				highlight: selectedText,
				element: highlightContainers,
			},
		]);
	};

	return (
		<button className="reset" onClick={startHighlighter} title="Highlighter">
			<MarkerIcon className="icon-sm" />
		</button>
	);
};

export default Highlighter;
