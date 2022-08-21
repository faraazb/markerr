import { h, Fragment } from "preact";
import { route } from "preact-router";
import { useEffect } from "preact/hooks";
import { getComments } from "../../annotator/api";
import { useStore } from "../../annotator/store";
import { Comment, CreateComment } from "../comment/comment";
import { UsersIcon, MarkerIcon, SipLineIcon, SearchIcon } from "../icons";

const Comments = (props) => {
	const { setPopupOpen } = props;
	const [site] = useStore.site();
	const [comments, setComments] = useStore.comments();
	const [currentPage] = useStore.currentPage();

	useEffect(() => {
		// get all root comments for the current page
		// console.log(site);
		if (site.data !== null) {
			if (currentPage in site.data.pages) {
				// if current page exists, get comments
				const page = site.data.pages[currentPage];
				(async () => {
					setComments({ ...comments, loading: true, error: false });
					try {
						const response = await getComments(page.id);
						setComments({ data: response, loading: false, error: false });
					} catch (e) {
						console.error(e);
						setComments({ ...comments, loading: false, error: true });
					}
				})();
			}
		}
	}, [site, currentPage]);

	// useEffect(() => {
	// 	console.log(comments)
	// }, [comments]);

	return (
		<>
			<div className="popup-header">
				<UsersIcon className="icon-md" />
				<span className="header-1">Comments</span>
				<div className="popup-header-actions">
					<button className="button-3" onClick={() => route("/login")}>
						Comment
					</button>
				</div>
			</div>
			<div className="popup-content">
				<CreateComment setPopupOpen={setPopupOpen} />
				<div className="search">
					<SearchIcon className="icon-sm" />
					<input
						className="reset search-bar"
						type="text"
						placeholder="Search.."
					/>
				</div>
				{comments.data !== null &&
					comments.data.map(
						({
							id,
							display_id,
							created,
							user,
							content,
							reply_to_id,
							parent_id,
							is_resolved,
							elements,
						}) => {
							return (
								<Comment
									key={id}
									id={id}
									created={created}
									user={user}
									displayId={display_id}
									content={content}
									replyToId={reply_to_id}
									parentId={parent_id}
									elements={elements}
									isResolved={is_resolved}
								/>
							);
						}
					)}
			</div>
		</>
	);
};

export default Comments;
