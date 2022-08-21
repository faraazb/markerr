import { h, Fragment } from "preact";
import { useEffect, useState } from "preact/hooks";
import history from "../history";
import axios from "redaxios";
import Comments from "../components/comments/comments";
import Replies from "../components/replies/replies";
import {
	MarkerIcon,
	SipLineIcon,
	SearchIcon,
	UsersIcon,
} from "../components/icons";
import "./annotator.css";
import Router, { Route, route } from "preact-router";
import Match from 'preact-router/match';

// import {people} from '../components/icons';
// import {Comment} from '../comment/comment';
// import {theRoom} from 'theroomjs';
import "theroomjs/dist/theroom.min.js";
import SuperTokens from 'supertokens-web-js';
import ThirdPartyEmailPassword from 'supertokens-web-js/recipe/thirdpartyemailpassword';
import Session from 'supertokens-web-js/recipe/session';
import Login from "../components/login/login";
import Signup from "../components/signup/signup";
import { useStore } from "./store";
import Site from "../components/site/site";
import { API_DOMAIN, api, getSite } from "./api";



export const Annotator = () => {
	// const [counter, setCounter] = useState(0)
	const [open, setOpen] = useState(false);
	const [site, setSite] = useStore.site();
	const [page, setPage] = useStore.currentPage();

	useEffect(() => {
		setPage(window.location.pathname);

		// initialize SuperTokens
		SuperTokens.init({
			appInfo: {
				appName: 'Markerr',
				apiDomain: API_DOMAIN,
				apiBasePath: '/auth',
			},
			recipeList: [ThirdPartyEmailPassword.init(), Session.init()],
		});

		// check if user is logged in
		async function checkSession() {
			if (!await Session.doesSessionExist()) {
				route("/login")
			}
			// else {
			// 	route("/comments")
			// }
		}

		checkSession();

		

		// get site data
		async function getCurrentSite() {
			console.log("getting current site")
			setSite({...site, loading: true, error: false});
			try {
				const siteData = await getSite(window.location.hostname);
				setSite({data: siteData, loading: false, error: false});
				console.log(site);
			}
			catch (e) {
				console.error(e);
				setSite({...site, loading: false, error: true});
			}
		}
		getCurrentSite();

		// poll for pathname changes, required when JS is changing paths, e.g. SPAs
		// comments will rerender
		// this causes a lot of rerendering investigate
		// setInterval(() => {
		// 	if (window.location.pathname !== page) setPage(window.location.pathname);
		// }, 100);

		// initialize the roomjs
		if (theRoom) {
			window.theRoom.configure({
				inspector: "#annotator-inspector",
				blockRedirection: true,
				excludes: ["#annotator-button"],
			});

			// window.theRoom.start();
			window.theRoom.on("hook", function (event) {
				event.preventDefault();
				if (
					event.target.id === "annotator-inspector-button" ||
					event.target.id === "annotator-inspector-button-icon"
				) {
					return false;
				}
			});
		}		
	}, []);

	const togglePopup = () => {
		setOpen(open === true ? false : true);
	};

	const getElementByXpath = (path) => {
		return document.evaluate(
			path,
			document,
			null,
			XPathResult.FIRST_ORDERED_NODE_TYPE,
			null
		).singleNodeValue;
	};

	const getElementByCssPath = (path) => {
		return document.querySelector(path);
	};

	const getComments = async () => {
		const response = await fetch(
			`${API}/comments/0d17eb3f-1e4f-4201-b070-d05a4533760c`
		);
		const data = await response.json();
		setUser(JSON.stringify(data));
	};

	return (
		<div id="annotator">
			<div className={`annotator-popup ${open === true ? "show" : ""}`}>
				<Router history={history}>
					<Signup path="/signup" />
					<Login path="/login" />
					<Site path="/site/:id?" />
                    <Replies path="/replies/:commentId" setPopupOpen={setOpen}/>
					<Comments path="/" setPopupOpen={setOpen}/>
				</Router>
			</div>
			<button id="annotator-button" className="button-30" onClick={togglePopup}>
				A
			</button>
		</div>
	);
};
