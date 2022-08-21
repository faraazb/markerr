import { h, Fragment } from "preact";
import { useEffect } from "preact/hooks";
import { getComments } from "../../annotator/api";
import { useStore } from "../../annotator/store";
import history from "../../history";
import { Comment, CreateComment } from "../comment/comment";
import { SearchIcon } from "../icons";


const Replies = (props) => {
	const { commentId, setPopupOpen } = props;
	const [site, ] = useStore.site();
	const [replies, setReplies] = useStore.replies();
	const [currentPage, ] = useStore.currentPage();

	useEffect(() => {
		if (!site.data) return;
		if (!currentPage in site.data.pages) return;
		const pageId = site.data.pages[currentPage].id;
		(async () => {
			setReplies({...replies, loading: true, error: false});
			try {
				const response = await getComments(pageId, commentId);
				setReplies({data: response, loading: false, error: false});
			}
			catch (e) {
				console.error(e)
				setReplies({...replies, loading: false, error: true});
			}
		})();
	}, [])

	return (
		<>
			<div className="popup-header">
				<span className="header-1">Replies #14</span>
				<div className="popup-header-actions">
					<button className="reset nav-button" onClick={history.back}>
						Back
					</button>
				</div>
			</div>
			<div className="popup-content">
				<CreateComment setPopupOpen={setPopupOpen} reply={true} />
				<div className="search">
					<SearchIcon className="icon-sm" />
					<input
						className="reset search-bar"
						type="text"
						placeholder="Search.."
					/>
				</div>
				<Comment content={"hello world"} replyTo={"sdhjs"}/>
				<Comment content={"hello world"} replyTo={"sdhjs"}/>
				<Comment content={"hello world"} replyTo={"sdhjs"}/>
				<Comment content={"hello world"} replyTo={"sdhjs"}/>
			</div>
		</>
	);
};

export default Replies;
