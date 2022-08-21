/*
 * Function to create an expath for an HTML element
 *
 *
 * By stijn de ryck (https://stackoverflow.com/users/642608/stijn-de-ryck)
 * https://stackoverflow.com/questions/2661818/javascript-get-xpath-of-a-node
 *
 */
function createXpath(elm) {
	var allNodes = document.getElementsByTagName("*");
	for (var segs = []; elm && elm.nodeType == 1; elm = elm.parentNode) {
		if (elm.hasAttribute("id")) {
			var uniqueIdCount = 0;
			for (var n = 0; n < allNodes.length; n++) {
				if (allNodes[n].hasAttribute("id") && allNodes[n].id == elm.id)
					uniqueIdCount++;
				if (uniqueIdCount > 1) break;
			}
			if (uniqueIdCount == 1) {
				segs.unshift('id("' + elm.getAttribute("id") + '")');
				return segs.join("/");
			} else {
				segs.unshift(
					elm.localName.toLowerCase() + '[@id="' + elm.getAttribute("id") + '"]'
				);
			}
		} else if (elm.hasAttribute("class")) {
			segs.unshift(
				elm.localName.toLowerCase() +
					'[@class="' +
					elm.getAttribute("class") +
					'"]'
			);
		} else {
			var i, sib;
			for (i = 1, sib = elm.previousSibling; sib; sib = sib.previousSibling) {
				if (sib.localName == elm.localName) i++;
			}
			segs.unshift(elm.localName.toLowerCase() + "[" + i + "]");
		}
	}
	let result = segs.length ? "/" + segs.join("/") : null;
	// remove classname added by theroom
	return result.replace('[@class=" theRoom"]', "");
}

/*
 * Function to transform given comment elements into the API compliant format
 * {rId, element, highlight}
 * An element can be a single HTML element or a group of HTML element
 * 
 */
function makeElements(elements) {
	let commentElements = [];
	for (const { element, highlight } of elements) {
		if (highlight) {
			for (const { el, text } of element) {
				commentElements.push({
					element: el.nodeName.toLowerCase(),
					css_selector: el.cssSelector,
					xpath: el.xpath,
					text_highlights: [
						{
							color: "yellow",
							content: text,
						},
					],
				});
			}
		} else {
			commentElements.push({
				element: element.nodeName.toLowerCase(),
				css_selector: element.cssSelector,
				xpath: element.xpath,
			});
		}
	}
    return commentElements;
}

export { createXpath, makeElements };
