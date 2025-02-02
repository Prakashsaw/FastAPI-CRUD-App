import React, { useState, useRef } from "react";
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

const validEmail = (value) => {
  if (!isEmail(value)) {
    return (
      <div className="invalid-feedback d-block">This is not a valid email.</div>
    );
  }
};

const SendResetPasswordLink = () => {
  const form = useRef();
  const checkBtn = useRef();

  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [successful, setSuccessful] = useState(false);

  const onChangeEmail = (e) => {
    const email = e.target.value;
    setEmail(email);
  };

  const handeSendResetPasswordLink = (e) => {
    e.preventDefault();

    setMessage("");
    setLoading(true);
    setSuccessful(false);

    form.current.validateAll();

    if (checkBtn.current.context._errors.length === 0) {
      AuthService.sendResetPasswordLink(email)
        .then((response) => {
          setMessage(response.data.message || "Account verified successfully!");
          setSuccessful(true);
        })
        .catch((error) => {
          const resMessage =
            error.response?.data?.detail ||
            "Verification failed. Try again later.";
          setMessage(resMessage);
          setSuccessful(false);
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  };

  return (
    <div className="col-md-12">
      <div className="card card-container">
        <Form onSubmit={handeSendResetPasswordLink} ref={form}>
          {!successful && (
            <div>
              <div className="form-group">
                <label htmlFor="email">Registered Email</label>
                <Input
                  type="text"
                  className="form-control"
                  name="email"
                  value={email}
                  onChange={onChangeEmail}
                  validations={[required, validEmail]}
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
                    <span>Send Reset Password Link</span>
                  )}
                </button>
              </div>

              <div className="form-group text-center">
                <Link to="/login">Back To Login</Link>
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

export default SendResetPasswordLink;
