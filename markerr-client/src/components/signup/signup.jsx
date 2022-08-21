import { h, Fragment } from "preact";
import { route } from "preact-router";
import { useEffect, useState } from "preact/hooks";
import "./signup.css";

const Signup = (props) => {
	const [email, setEmail] = useState();
	const [password, setPassword] = useState();

	// useEffect(() => {

	// }, [])

	const signup = async () => {
		// validation
		const response = await ThirdPartyEmailPassword.emailPasswordSignUp({
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
		console.log(response);
	};

	return (
		<div className="form">
			<div className="header">Signup</div>
			<div className="fields">
				<div className="field">
					<label for="field-signup-username">Username</label>
					<input
						id="field-signup-username"
						className="reset"
						name="username"
						required
					></input>
				</div>
				<div className="field-group">
					<div className="field">
						<label for="field-signup-fname">First Name</label>
						<input
							id="field-signup-fname"
							className="reset"
							name="fname"
							required
						></input>
					</div>
					<div className="field">
						<label for="field-signup-lname">Last Name</label>
						<input
							id="field-signup-lname"
							className="reset"
							name="lname"
							required
						></input>
					</div>
				</div>
				<div className="field">
					<label for="field-signup-email">Email</label>
					<input
						id="field-signup-email"
						className="reset"
						name="email"
						type="email"
						required
					></input>
				</div>
				<div className="field">
					<label for="field-signup-password">Password</label>
					<input
						id="field-signup-password"
						className="reset"
						name="password"
						type="password"
						required
					></input>
				</div>
			</div>
			<div className="submit">
				<button className="button button-primary button-block button-sm">
					Signup
				</button>
			</div>
			<div className="actions">
				<button className="reset nav-button" onClick={() => route("/login")}>
					Login
				</button>
			</div>
		</div>
	);
};

export default Signup;
