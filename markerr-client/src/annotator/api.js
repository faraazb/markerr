import axios from "redaxios";

// TODO: needs better error handling

const API_DOMAIN = "http://annotator.test";
const SUCCESS = "success";
const FAIL = "fail";
const ERROR = "error";

const api = axios.create({
	baseURL: API_DOMAIN,
});

async function getSite(domain) {
    try {
        const response = await api.get('/sites/', {
            params: {
                domain: domain
            },
            withCredentials: true
        });
        if (response.data) {
            // if site doesn't exist, allow local annotations
            if (response.data.status === SUCCESS) {
                return response.data.data;
            }
        }
    }
    catch (e) {
        throw e;
    }
}

async function getComments(pageId, commentId) {
    if (!pageId) {
        console.error("rejected ", pageId)
        return null;
    }
    let url = `/comments/${pageId}`;
    if (commentId) {
        url = `/comments/${pageId}/${commentId}`;
    }
    try {
        console.log(`API GET: ${url}`)
        const response = await api.get(url, {withCredentials: true});
        if (response.data) {
            if (response.data.status === SUCCESS) {
                return response.data.data;
            }
            else {
                return null;
            }
        }
    }
    catch (e) {
        throw e;
    }
}


async function createPage(page) {
    if (!page) {
        console.error("rejected")
        return null;
    }
    const {siteId, url} = page;
    try {
        const response = await api.post("/pages/", {site_id: siteId, url: url}, {withCredentials: true});
        if (response.data) {
            if (response.data.status === SUCCESS) {
                return response.data.data;
            }
            else {
                return null;
            }
        }
    }
    catch (e) {
        throw e;
    }
}

export { API_DOMAIN, api, getSite, getComments };
