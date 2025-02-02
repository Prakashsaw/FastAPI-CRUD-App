import React, { useState, useRef } from "react";
import Form from "react-validation/build/form";
import Input from "react-validation/build/input";
import CheckButton from "react-validation/build/button";

import { useSearchParams } from "react-router-dom";

import AuthService from "../services/auth.service";

const required = (value) => {
  if (!value) {
    return (
      <div className="invalid-feedback d-block">This field is required!</div>
    );
  }
};

const vpassword = (value) => {
  if (value.length < 8 || value.length > 40) {
    return (
      <div className="invalid-feedback d-block">
        The password must be between 8 and 40 characters.
      </div>
    );
  }
};

const ResetPassword = (props) => {
  const form = useRef();
  const checkBtn = useRef();

  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  //   const email = searchParams.get("email");

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [successful, setSuccessful] = useState(false);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const onChangePassword = (e) => {
    const password = e.target.value;
    setPassword(password);
  };

  const onChangeConfirmPassword = (e) => {
    const confirmPassword = e.target.value;
    setConfirmPassword(confirmPassword);
  };

  const handleResetPassword = (e) => {
    e.preventDefault();

    setMessage("");
    setSuccessful(false);
    setLoading(true);

    form.current.validateAll();

    if (checkBtn.current.context._errors.length === 0) {
      if (password !== confirmPassword) {
        setMessage("Passwords and ConfirmPassword don't match!");
        setSuccessful(false);
        setLoading(false);
        return;
      }

      AuthService.resetPassword(token, password).then(
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
        <h3 style={{ marginBottom: "30px" }}>Reset Password</h3>
        <Form onSubmit={handleResetPassword} ref={form}>
          {!successful && (
            <div>
              <div className="form-group">
                <label htmlFor="password">New Password</label>
                <Input
                  type="password"
                  className="form-control"
                  name="password"
                  value={password}
                  onChange={onChangePassword}
                  validations={[required, vpassword]}
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
                  //   validations={[required, vpassword]}
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
                    <span>Reset Password</span>
                  )}
                </button>
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

export default ResetPassword;
