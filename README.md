# Markerr
Marker is a webpage annotation tool.
I am building it for Contentstack's Techsurf 2022 competition.

This repository consists of a Flask API and a JS client. The client can built into a library to be included in other sites.

[Supertokens](https://supertokens.com/) is used for authentication and authorization. Authentication cookies (SameSite set to None) are stored on each host website that the client can use to authenticate with the API.

The client uses the Preact framework and is bundled into a library using [Microbundle](https://github.com/developit/microbundle).

## Concept
- A site refers to any domain name (example.com, eg.example.com count as seperate sites).
- A site can have pages (example.com/blog, example.com/app, etc.).
- Pages can be commented on by authorized users. (Replying, resolving)

    A comment response from the API looks like this:
    ```json
    {
        "content": "\"The quick brown fox jumps over the lazy dog\"",
        "created": "Sun, 21 Aug 2022 14:37:00 GMT",
        "display_id": 4,
        "elements": [
            {
                "css_selector": "h1",
                "element": "h1",
                "id": "5a877e87-6d27-46b1-874a-60ebd8e93914",
                "text_highlights": [
                    {
                        "color": "yellow",
                        "content": "quick brown fox jumps",
                        "id": "3508a99e-ccce-4418-bce4-f70e0c57a254"
                    }
                ],
                "xpath": "/html[1]/body[1]/h1[1]"
            },
            {
                "css_selector": "button:nth-child(5)",
                "element": "button",
                "id": "cd51238b-9b9c-4fb1-827d-ca25b68734fa",
                "text_highlights": [],
                "xpath": "/html/body[1]/button[1]"
            }
        ],
        "id": "db8c15b1-c501-4232-b122-a6134787cce8",
        "is_deleted": false,
        "is_resolved": false,
        "parent_id": null,
        "reply_to_id": null,
        "updated": "Sun, 21 Aug 2022 14:37:00 GMT",
        "user": {
            "full_name": "Faraaz B",
            "id": "befcd593-a715-418c-91f1-9e312d3279af",
            "short_name": "Faraaz",
            "username": "faraaz"
        }
    }
    ```


## Completed
- The API is ready with core features.
- With the client, a user can display comments and select HTML elements, highlight text spanning across multiple HTML elements and attach them while posting comments.

## Pending
- Resolving comments
- Site controlling and team functionalities

## Deployment
The only way to try it out is by running everything locally.

API has been deployed at [markerrdev.herokuapp.com](markerrdev.herokuapp.com) which has been tested with Postman but not through the client/script from a secure (HTTPS) test site which embeds the client. It is expected to work considering the cookie settings on the backend.

## Running locally
### Requirements
- PostgreSQL
- Python (developed on 3.10)
- Node
- SuperTokens (can also use a [managed instance](https://supertokens.com/dashboard-saas))

### Setup
1. Create a database and update [`config.py`](https://github.com/faraazb/markerr/blob/main/markerr/markerr/config.py).
2. Install and [setup SuperTokens](https://supertokens.com/docs/thirdpartyemailpassword/quick-setup/core/without-docker) by updating database details in its config.
    
    OR

    Signup for a managed instance and update [`config.py`](https://github.com/faraazb/markerr/blob/main/markerr/markerr/config.py) with api key. 
3. Create tables using `flask initdb` by navigating to markerr and setting FLASK env variables (FLASK_APP=markerr.app, FLASK_ENV=development)
4. Create a user and a site (name=localhost) owned by this user.
5. Navigate to markerr-client and run `npm install`.
6. Run `npm run dev` and navigate to localhost:5100.

    To build the library, run `npm build:widget`

### Additional setup
- To test multiple sites, I changed my DNS settings (hosts file) and used Apache server to create virtual hosts with dummy domains (example.test, markerr.test) resolving to different ports on localhost.