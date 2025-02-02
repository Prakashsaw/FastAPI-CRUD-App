import React, { useState, useRef } from "react";
import Form from "react-validation/build/form";
import CheckButton from "react-validation/build/button";

import { useSearchParams } from "react-router-dom";

import AuthService from "../services/auth.service";

const UserAccountVerify = () => {
  const form = useRef();
  const checkBtn = useRef();

  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const email = searchParams.get("email");

  const [message, setMessage] = useState("");
  const [successful, setSuccessful] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleVerify = (e) => {
    e.preventDefault();

    setMessage("");
    setSuccessful(false);
    setLoading(true);

    form.current.validateAll();
    if (checkBtn.current.context._errors.length === 0) {
      AuthService.verifyAccount(token, email)
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
        <h3 style={{ marginBottom: "30px" }}>Account Verification</h3>
        <Form onSubmit={handleVerify} ref={form}>
          {!successful && (
            <div className="form-group">
              <button className="btn btn-primary btn-block" disabled={loading}>
                {loading ? (
                  <span className="spinner-border spinner-border-sm"></span>
                ) : (
                  <span>Click Here To Verify Your Account</span>
                )}
              </button>
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

export default UserAccountVerify;
