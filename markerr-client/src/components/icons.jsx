import { h, Fragment } from "preact";


const SipLineIcon = (props) => {
	const { className } = props;

	let classes = "";
	if (className) {
		classes = " " + className;
	}

	return (
		<svg
			className={`icon${classes}`}
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 24 24"
			width="24"
			height="24"
		>
			<path fill="none" d="M0 0h24v24H0z" />
			<path d="M6.457 18.957l8.564-8.564-1.414-1.414-8.564 8.564 1.414 1.414zm5.735-11.392l-1.414-1.414 1.414-1.414 1.768 1.767 2.829-2.828a1 1 0 0 1 1.414 0l2.121 2.121a1 1 0 0 1 0 1.414l-2.828 2.829 1.767 1.768-1.414 1.414-1.414-1.414L7.243 21H3v-4.243l9.192-9.192z" />
		</svg>
	);
};

const MarkerIcon = (props) => {
	const { className } = props;

	let classes = "";
	if (className) {
		classes = " " + className;
	}

	return (
		<svg
			className={`icon${classes}`}
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 24 24"
			width="24"
			height="24"
		>
			<path fill="none" d="M0 0h24v24H0z" />
			<path d="M15.243 4.515l-6.738 6.737-.707 2.121-1.04 1.041 2.828 2.829 1.04-1.041 2.122-.707 6.737-6.738-4.242-4.242zm6.364 3.535a1 1 0 0 1 0 1.414l-7.779 7.779-2.12.707-1.415 1.414a1 1 0 0 1-1.414 0l-4.243-4.243a1 1 0 0 1 0-1.414l1.414-1.414.707-2.121 7.779-7.779a1 1 0 0 1 1.414 0l5.657 5.657zm-6.364-.707l1.414 1.414-4.95 4.95-1.414-1.414 4.95-4.95zM4.283 16.89l2.828 2.829-1.414 1.414-4.243-1.414 2.828-2.829z" />
		</svg>
	);
};

const ArrowDropRightIcon = (props) => {
	const { className } = props;

	let classes = "";
	if (className) {
		classes = " " + className;
	}

	return (
		<svg
			className={`icon${classes}`}
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 24 24"
			width="24"
			height="24"
		>
			<path fill="none" d="M0 0h24v24H0z" />
			<path d="M12.172 12L9.343 9.172l1.414-1.415L15 12l-4.243 4.243-1.414-1.415z" />
		</svg>
	);
};

const SearchIcon = (props) => {
	const { className } = props;
	let classes = "";
	if (className) {
		classes = " " + className;
	}

	return (
		<svg
			className={`icon${classes}`}
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 24 24"
			width="24"
			height="24"
		>
			<path fill="none" d="M0 0h24v24H0z" />
			<path d="M18.031 16.617l4.283 4.282-1.415 1.415-4.282-4.283A8.96 8.96 0 0 1 11 20c-4.968 0-9-4.032-9-9s4.032-9 9-9 9 4.032 9 9a8.96 8.96 0 0 1-1.969 5.617zm-2.006-.742A6.977 6.977 0 0 0 18 11c0-3.868-3.133-7-7-7-3.868 0-7 3.132-7 7 0 3.867 3.132 7 7 7a6.977 6.977 0 0 0 4.875-1.975l.15-.15z" />
		</svg>
	);
};

const UsersIcon = (props) => {
    const { className } = props;
	let classes = "";
	if (className) {
		classes = " " + className;
	}

	return (
		<svg
            className={`icon${classes}`}
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 16 16"
			width="16"
			height="16"
		>
			<path
				fill-rule="evenodd"
				d="M5.5 3.5a2 2 0 100 4 2 2 0 000-4zM2 5.5a3.5 3.5 0 115.898 2.549 5.507 5.507 0 013.034 4.084.75.75 0 11-1.482.235 4.001 4.001 0 00-7.9 0 .75.75 0 01-1.482-.236A5.507 5.507 0 013.102 8.05 3.49 3.49 0 012 5.5zM11 4a.75.75 0 100 1.5 1.5 1.5 0 01.666 2.844.75.75 0 00-.416.672v.352a.75.75 0 00.574.73c1.2.289 2.162 1.2 2.522 2.372a.75.75 0 101.434-.44 5.01 5.01 0 00-2.56-3.012A3 3 0 0011 4z"
			></path>
		</svg>
	);
};

export { SipLineIcon, MarkerIcon, ArrowDropRightIcon, SearchIcon, UsersIcon };
