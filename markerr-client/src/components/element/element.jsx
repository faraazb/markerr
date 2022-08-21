import { h, render } from "preact";
import { CloseLineIcon, MarkerIcon, SipLineIcon } from "../icons";

const Element = (props) => {
	const { element, highlight, cssSelector, xpath, remove } = props;

	const highlightElement = () => {
		if (Array.isArray(element)) {
			// highlight spanning across multiple HTML nodes
			// then element is a list of 'highlightContainers' {el: HTMLNode, text: "hello wor"}
			for (const container of element) {
				container.el.innerHTML = container.el.innerHTML.replace(
					container.text,
					`<span class="annotator-text-highlight">${container.text}</span>`
				);
			}
		} else if (!Array.isArray(element) && highlight) {
			// highlight bounded within a single HTML node
			element.innerHTML = element.innerHTML.replace(
				highlight,
				`<span class="annotator-text-highlight">${highlight}</span>`
			);
		} else {
			// just an HTML node
			element.style.outline = "2px dashed red";
			element.style.outlineOffset = "0.6rem";
			element.scrollIntoView({
				behavior: "smooth",
				block: "center",
				inline: "center",
			});
		}
	};

	const resetElement = () => {
		if (Array.isArray(element)) {
			for (const container of element) {
				container.el.innerHTML = container.el.innerHTML.replace(
					`<span class="annotator-text-highlight">${container.text}</span>`,
					container.text
				);
			}
		} else if (!Array.isArray(element) && highlight) {
			element.innerHTML = element.innerHTML.replace(
				`<span class="annotator-text-highlight">${highlight}</span>`,
				highlight
			);
		} else {
			element.style.outline = "revert";
			element.style.outlineOffset = "revert";
		}
	};

	const removeSelf = () => {
		resetElement();
		remove(cssSelector);
	}

	return (
		<div
			className="chip element"
			onMouseEnter={highlightElement}
			onMouseLeave={resetElement}
		>
			{!highlight && (
				<>
					<SipLineIcon className="icon-sm" />
					{element.nodeName.toLowerCase()}
				</>
			)}
			{highlight && (
				<>
					<MarkerIcon className="icon-sm" />
					Highlight
				</>
			)}
			{remove && (
				<button
					className="reset"
					onClick={removeSelf}
					title="Remove"
				>
					<CloseLineIcon className="icon-sm" />
				</button>
			)}
		</div>
	);
};

export default Element;
