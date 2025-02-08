import React, { useState, useRef } from "react";
import { useNavigate, Link } from "react-router-dom";
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

const Login = () => {
  const form = useRef();
  const checkBtn = useRef();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  const onChangeEmail = (e) => {
    const email = e.target.value;
    setEmail(email);
  };

  const onChangePassword = (e) => {
    const password = e.target.value;
    setPassword(password);
  };

  const handleLogin = (e) => {
    e.preventDefault();

    setMessage("");
    setLoading(true);

    form.current.validateAll();

    if (checkBtn.current.context._errors.length === 0) {
      if (!isEmail(email)) {
        setMessage(
          "Please enter a valid email address. Examples: test_email@domain.com, example@gmail.com, etc..."
        );
        setLoading(false);
        return;
      }

      if (password.length < 8) {
        setMessage(
          "The password must be 8 characters long. It must contain at least one uppercase letter, one lowercase letter, one number and one special character. Examples: Abc@1234, Strong_Password#1, etc..."
        );
        setLoading(false);
        return;
      }

      AuthService.login(email, password).then(
        (response) => {
          // console.log("response", response);
          if (response.user.is_verified === false) {
            setMessage(response.message);
            setLoading(false);
            return;
          }
          navigate("/profile");
          window.location.reload();
        },
        (error) => {
          const resMessage =
            (error.response &&
              error.response.data &&
              error.response.data.detail) ||
            error.message ||
            error.toString();

          setLoading(false);
          setMessage(resMessage);
        }
      );
    } else {
      setLoading(false);
    }
  };

  return (
    <div className="col-md-12">
      <div className="card card-container">
        <img
          src="//ssl.gstatic.com/accounts/ui/avatar_2x.png"
          alt="profile-img"
          className="profile-img-card"
        />

        <Form onSubmit={handleLogin} ref={form}>
          <div className="form-group">
            <label htmlFor="email">Username or Email</label>
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
            <button className="btn btn-primary btn-block" disabled={loading}>
              {loading ? (
                <span className="spinner-border spinner-border-sm"></span>
              ) : (
                <span>Login</span>
              )}
            </button>
          </div>

          <div className="form-group text-center">
            <Link to="/send-reset-password-link">Forgot Password?</Link>
          </div>

          <div className="form-group text-center">
            Don't have an account?<Link to="/register"> Sign Up</Link>
          </div>

          {message && (
            <div className="form-group">
              <div className="alert alert-danger" role="alert">
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

export default Login;
