import { h, Fragment } from "preact";
import { route } from "preact-router";
import { useEffect, useState } from "preact/hooks";
import ThirdPartyEmailPassword from "supertokens-web-js/recipe/thirdpartyemailpassword";
import { useStore } from "../../annotator/store";

const Login = (props) => {
	const [email, setEmail] = useState();
	const [password, setPassword] = useState();
	const [user, setUser] = useStore.user();
	const [error, setError] = useState();

	// useEffect(() => {

	// }, [])

	const login = async (event) => {
		event.preventDefault();
		setUser({ ...user, loading: true });
		if (
			email === "" ||
			password === "" ||
			email === undefined ||
			password === undefined
		) {
            // should never come here
			return;
		}
		try {
            const signin = await ThirdPartyEmailPassword.emailPasswordSignIn({
                formFields: [
                    {
                        id: "email",
                        value: email,
                    },
                    {
                        id: "password",
                        value: password,
                    },
                ],
            });
            const response = await signin.fetchResponse.json();
            setUser({ data: response.data.user, loading: false, error: false });
            route("/");
        }
        catch (e) {
            const response = await e.json();
            console.log(response);
            if (response.status === "fail") {
                setError(response.message);
            }
            return;
        }
	};

	return (
		<form className="form" onSubmit={login}>
			<div className="header">Login</div>
			<div className="field">
				<label for="field-login-email">Email</label>
				<input
					id="field-login-email"
					className="reset"
					name="email"
					type="email"
					onChange={(e) => setEmail(e.target.value)}
					required
				></input>
			</div>
			<div className="field">
				<label for="field-login-password">Password</label>
				<input
					id="field-login-password"
					className="reset"
					name="password"
					type="password"
					onChange={(e) => setPassword(e.target.value)}
					required
				></input>
			</div>
			<div className="submit">
				<button
					className="button button-primary button-block button-sm"
					type="submit"
				>
					Login
				</button>
			</div>
			{error && <div className="form-error">{error}</div>}
			<div>
				<button className="reset nav-button" onClick={() => route("/signup")}>
					Signup
				</button>
			</div>
		</form>
	);
};

export default Login;
