import { h, Fragment } from "preact";
import { route } from "preact-router";
import { useEffect, useState } from "preact/hooks";
import "theroomjs/dist/theroom.min.js";
import { SipLineIcon, MarkerIcon, ArrowDropRightIcon } from "../icons";
import "./comment.css";


const Comment = (props) => {
	// const { id, user, displayId, content, replyTo, elements } = props;
	const { id, content, replyTo } = props;

	return (
		<div className="comment">
			<div className="title">
				<div className="username" title="Faraaz Biyabani">
					faraaz
				</div>
				<div className="time">6 hours ago</div>
				{!replyTo && (
					<div
						className="nav-button replies-link"
						onClick={() => route(`/replies/${id}`)}
					>
						<span>Replies</span>
						<ArrowDropRightIcon className="icon-sm" />
					</div>
				)}
			</div>
			{replyTo && (
				<div className="reply-to">
					<div className="reply-to-heading">
						<MarkerIcon className="icon-sm" />
						<span>Reply to #{replyTo}</span>
					</div>
					<div className="reply-to-content">The quick brown fox jumps over</div>
				</div>
			)}
			<div className="content">
				{content}
			</div>
			<div className="attachments">
				<div className="chip">
					<SipLineIcon className="icon-sm" />
					<span>button-1</span>
				</div>
				<div className="chip">
					<SipLineIcon className="icon-sm" />
					<span>button-1</span>
				</div>
				<div className="chip">
					<MarkerIcon className="icon-sm" />
					<span>heading</span>
				</div>
			</div>
		</div>
	);
};

const CreateComment = (props) => {
	const { setPopupOpen, reply = false } = props;
	const [elements, setElements] = useState([]);

	useEffect(() => {
		// whenever elements changes, this rerenders
		console.log("rendered")
		if (theRoom) {
			window.theRoom.on("click", function (element, event) {
				console.log("Selected element", element);
				setElements([...elements, element])
				window.theRoom.stop(true);
			});
		}
	}, []);

	useEffect(() => {
		console.log(elements);
	}, [elements]);

	useEffect(() => {
		console.log("rendered again")
	})

	const startInspector = () => {
		window.theRoom.start();
		setPopupOpen(false);
	};

	const startHighlighter = () => {
		console.log("starting highlighter");
		const handleSelection = () => {
			console.log("got selection");
			const selection = window.getSelection();
			if (!selection.rangeCount) return;

			const range = selection.getRangeAt(0);

			console.log("Selected elements:");
			range
				.cloneContents()
				.querySelectorAll("*")
				.forEach((element) => {
					console.log(element);
					// highlightedText = element.innerText
					// element.outerHTML = (
					// 	<span class="annotator-text-highlight">${highlightedText}</span>
					// );

					// create wrapper container
					// var wrapper = document.createElement("span");
					// wrapper.className = "annotator-text-highlight"
					// // insert wrapper before el in the DOM tree
					// element.parentNode.insertBefore(wrapper, element);
					// // move el into wrapper
					// wrapper.appendChild(element);
				});
		};
		document.addEventListener("mouseup", handleSelection, { once: true });
	};

	let buttonLabel = "Comment";
	if (reply === true) {
		buttonLabel = "Reply";
	}

	return (
		<div className="new-comment">
			<div className="input">
				<textarea className="reset" placeholder="Type here.."></textarea>
			</div>
			<div className="action-bar">
				<button
					id="annotator-inspector-button"
					className="reset"
					onClick={startInspector}
					title="Pick an HTML element"
				>
					<SipLineIcon
						id="annotator-inspector-button-icon"
						className="icon-sm"
					/>
				</button>
				<button
					className="reset"
					onClick={startHighlighter}
					title="Highlighter"
				>
					<MarkerIcon className="icon-sm" />
				</button>
				<button className="button button-primary button-sm">
					{buttonLabel}
				</button>
			</div>
		</div>
	);
};

export { Comment, CreateComment };
