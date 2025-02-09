import React, { useState, useRef} from "react";
import { Link } from "react-router-dom";
import Form from "react-validation/build/form";
import Input from "react-validation/build/input";
import CheckButton from "react-validation/build/button";
import { isEmail } from "validator";

import AuthService from "../services/auth.service";

const required = (value) => {
  if (!value) {
    return (
      <div className="invalid-feedback d-block">This field is required!</div>
    );
  }
};

const vusername = (value) => {
  if (value.length < 3 || value.length > 20) {
    return (
      <div className="invalid-feedback d-block">
        The username must be between 3 and 20 characters.
      </div>
    );
  }
};

// const validEmail = (value) => {
//   if (!isEmail(value)) {
//     return (
//       <div className="invalid-feedback d-block">This is not a valid email.</div>
//     );
//   }
// };

// const vpassword = (value) => {
//   if (value.length < 8 || value.length > 40) {
//     return (
//       <div className="invalid-feedback d-block">
//         The password must be between 8 and 40 characters.
//       </div>
//     );
//   }
// };

const Register = (props) => {
  const form = useRef();
  const checkBtn = useRef();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [successful, setSuccessful] = useState(false);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const onChangeUsername = (e) => {
    const username = e.target.value;
    setUsername(username);
  };

  const onChangeEmail = (e) => {
    const email = e.target.value;
    setEmail(email);
  };

  const onChangePassword = (e) => {
    const password = e.target.value;
    setPassword(password);
  };

  const onChangeConfirmPassword = (e) => {
    const confirmPassword = e.target.value;
    setConfirmPassword(confirmPassword);
  };

  const handleRegister = (e) => {
    e.preventDefault();

    setMessage("");
    setSuccessful(false);
    setLoading(true);

    form.current.validateAll();

    if (checkBtn.current.context._errors.length === 0) {
      if (!isEmail(email)) {
        setMessage(
          "Please enter a valid email address. Examples: test_email@domain.com, example@gmail.com, etc..."
        );
        setSuccessful(false);
        setLoading(false);
        return;
      }

      if (password.length < 8) {
        setMessage(
          "The password must be 8 characters long. It must contain at least one uppercase letter, one lowercase letter, one number and one special character. Examples: Abc@1234, Strong_Password#1, etc..."
        );
        setSuccessful(false);
        setLoading(false);
        return;
      }
      if (password !== confirmPassword) {
        setMessage("Passwords and ConfirmPassword don't match!");
        setSuccessful(false);
        setLoading(false);
        return;
      }

      AuthService.register(username, email, password).then(
        (response) => {
          setMessage(response.data.message);
          setSuccessful(true);
        },
        (error) => {
          const resMessage =
            (error.response &&
              error.response.data &&
              error.response.data.detail) ||
            error.message ||
            error.toString();

          setMessage(resMessage);
          setSuccessful(false);
          setLoading(false);
        }
      );
    } else {
      setLoading(false);
    }
  };

  return (
    <div className="col-md-12">
      <div className="card card-container">
        <Form onSubmit={handleRegister} ref={form}>
          {!successful && (
            <div>
              <img
                src="//ssl.gstatic.com/accounts/ui/avatar_2x.png"
                alt="profile-img"
                className="profile-img-card"
              />
              <div className="form-group">
                <label htmlFor="username">Name</label>
                <Input
                  type="text"
                  className="form-control"
                  name="name"
                  value={username}
                  onChange={onChangeUsername}
                  validations={[required, vusername]}
                />
              </div>

              <div className="form-group">
                <label htmlFor="email">Email</label>
                <Input
                  type="text"
                  className="form-control"
                  name="email"
                  value={email}
                  onChange={onChangeEmail}
                  validations={[required]}
                />
              </div>

              <div className="form-group">
                <label htmlFor="password">Password</label>
                <Input
                  type="password"
                  className="form-control"
                  name="password"
                  value={password}
                  onChange={onChangePassword}
                  validations={[required]}
                />
              </div>
              <div className="form-group">
                <label htmlFor="confirm-password">Confirm Password</label>
                <Input
                  type="password"
                  className="form-control"
                  name="confirm-password"
                  value={confirmPassword}
                  onChange={onChangeConfirmPassword}
                  validations={[required]}
                />
              </div>

              <div className="form-group">
                <button
                  className="btn btn-primary btn-block"
                  disabled={loading}
                >
                  {loading ? (
                    <span className="spinner-border spinner-border-sm"></span>
                  ) : (
                    <span>Sign Up</span>
                  )}
                </button>
              </div>
              <div className="form-group text-center">
                Already have an account?<Link to="/login"> Login</Link>
              </div>
            </div>
          )}

          {message && (
            <div className="form-group">
              <div
                className={
                  successful ? "alert alert-success" : "alert alert-danger"
                }
                role="alert"
              >
                {message}
              </div>
            </div>
          )}
          <CheckButton style={{ display: "none" }} ref={checkBtn} />
        </Form>
      </div>
    </div>
  );
};

export default Register;
