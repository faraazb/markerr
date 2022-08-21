import { h, Fragment } from "preact";
import { route } from "preact-router";
import { useState } from "preact/hooks";
import "./comment.css";
import "theroomjs/dist/theroom.min.js";
import { createComment, createPage } from "../../annotator/api";
import { MarkerIcon, ArrowDropRightIcon } from "../icons";
import Element from "../element/element";
import { makeElements } from "../../annotator/utils";
import Selector from "../selector/selector";
import Highlighter from "../highlighter/highlighter";
import { useStore } from "../../annotator/store";

const Comment = (props) => {
	const {
		id,
		created,
		user,
		displayId,
		content,
		replyToId,
		parentId,
		elements,
		isResolved,
	} = props;

	let commentElements = [];
	if (elements) {
		for (const {
			id: eId,
			element,
			css_selector,
			xpath,
			text_highlights,
		} of elements) {
			// console.log(text_highlights)
			let targetElement = document.querySelectorAll(css_selector)[0];
			if (targetElement) {
				if (text_highlights.length > 0) {
					// multiple 'disconnected' highlights per element can be supported
					// but not yet implemented
					commentElements.push({
						id: eId,
						element: targetElement,
						highlight: text_highlights[0].content,
						cssSelector: css_selector,
						xpath: xpath,
					});
				} else {
					commentElements.push({
						id: eId,
						element: targetElement,
						cssSelector: css_selector,
						xpath: xpath,
					});
				}
			}
		}
	}

	return (
		<div className="comment">
			<div className="title">
				<div className="username" title={user.full_name}>
					{user.username}
				</div>
				<div className="time">{created}</div>
				{!replyToId && (
					<div
						className="nav-button replies-link"
						onClick={() => route(`/replies/${id}`)}
					>
						<span>Replies</span>
						<ArrowDropRightIcon className="icon-sm" />
					</div>
				)}
			</div>
			{replyToId && (
				<div className="reply-to">
					<div className="reply-to-heading">
						<MarkerIcon className="icon-sm" />
						<span>Reply to #{replyToId}</span>
					</div>
					<div className="reply-to-content">{content}</div>
				</div>
			)}
			<div className="attachments">
				{commentElements.length !== 0 &&
					commentElements.map(
						({ id, element, highlight, cssSelector, xpath }) => {
							return (
								<Element
									key={id}
									element={element}
									highlight={highlight}
									cssSelector={cssSelector}
									xpath={xpath}
								/>
							);
						}
					)}
			</div>
			<div className="content">{content}</div>
			<div className="actions"><button className="reset button button-secondary">Resolve</button></div>
		</div>
	);
};

const CreateComment = (props) => {
	const { setPopupOpen, reply = false } = props;
	const [currentPage] = useStore.currentPage();
	const [site] = useStore.site();
	const [comments, setComments] = useStore.comments();
	const [elements, setElements] = useState([]);
	const [content, setContent] = useState("");

	let buttonLabel = "Comment";
	if (reply === true) {
		buttonLabel = "Reply";
	}

	const remove = (cssSelector) => {
		setElements((elements) =>
			elements.filter((el) => el.cssSelector !== cssSelector)
		);
	};

	async function postComment() {
		if (content === "") return;
		// if using local storage then do something else
		let pageId;
		if (!currentPage in site.data.pages) {
			const newPage = await createPage({siteId: site.id, url: currentPage})
			if (newPage) {
				pageId = newPage.id
			}
			else {
				return;
			}
		}
		else {
			pageId = site.data.pages[currentPage].id;
		}

		let commentElements = makeElements(elements);
		// console.log(commentElements)
		try {
			console.log("posting a comment");
			const createdComment = await createComment(pageId, {
				content: content,
				elements: commentElements,
			});
			if(createdComment) {
				setComments([...comments, createdComment]);
			}
		} catch (e) {
			// show message to user
			console.error(e);
		}
	}

	return (
		<div className="new-comment">
			<div className="input">
				<textarea
					className="reset"
					placeholder="Type here.."
					onChange={(e) => setContent(e.target.value)}
				></textarea>
			</div>
			<div className="attachments elements">
				{elements.length !== 0 &&
					elements.map(({ rId, element, highlight, cssSelector, xpath }) => {
						return (
							<Element
								key={rId}
								element={element}
								highlight={highlight}
								cssSelector={cssSelector}
								xpath={xpath}
								remove={remove}
							/>
						);
					})}
			</div>
			<div className="action-bar">
				<Selector setPopupOpen={setPopupOpen} setElements={setElements} />
				<Highlighter setElements={setElements} />
				<button
					className="button button-primary button-sm"
					onClick={postComment}
				>
					{buttonLabel}
				</button>
			</div>
		</div>
	);
};

export { Comment, CreateComment };
