import createStore from "teaful";

// export const { useStore } = createStore({
	
// 	images: [],
// 	loading: true,
// 	error: false,
// });

// replies: {
//     'jkdjfk': {
//         loading: false,
//         error: null
//     }
// }

export const { useStore } = createStore({
    currentPage: null,
	user: {
        data: null,
		loading: false,
		error: false
	},
    site: {
        data: null,
		loading: false,
		error: false
    },
    comments: {
        data: null,
        loading: false,
        error: false
    },
    replies: {
        data: null,
        loading: false,
        error: false
    }
});
