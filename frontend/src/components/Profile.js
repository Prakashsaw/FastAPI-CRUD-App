import React, { useState, useEffect } from "react";
import AuthService from "../services/auth.service";

const Profile = () => {
  const [currentUser, setCurrentUser] = useState(AuthService.getCurrentUser());
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    // Check if token is expired
    const checkTokenExpiry = () => {
      const user = AuthService.getCurrentUser();
      // console.log("user", user);
      // console.log("jwt_access_token", user.jwt_access_token);
      // console.log("isTokenExpired", AuthService.isTokenExpired(user.jwt_access_token));
      if (user && AuthService.isTokenExpired(user.jwt_access_token)) {
        setShowModal(true);
      }
    };

    checkTokenExpiry();
    const interval = setInterval(checkTokenExpiry, 30000); // Check in every 30 seconds for access token expiry

    return () => clearInterval(interval);
  }, []);

  const handleRefreshToken = async () => {
    try {
      const refreshedUser = await AuthService.refreshToken();
      setCurrentUser(refreshedUser);
      setShowModal(false);
    } catch (error) {
      console.error("Failed to refresh token", error);
      // handleLogout();
    }
  };

  const handleLogout = () => {
    AuthService.logout();
    window.location.href = "/login"; // Redirect to login page
  };

  return (
    <div className="container">
      <header className="jumbotron">
        <h3>
          <strong>{currentUser.user.name}</strong> Profile
        </h3>
      </header>
      <p>
        <strong>Name:</strong> {currentUser.user.name}
      </p>
      <p>
        <strong>Email:</strong> {currentUser.user.email}
      </p>
      <p>
        <strong>User Id:</strong> {currentUser.user.user_id}
      </p>

      <strong>Authorities:</strong>
      {/* <ul>
        {currentUser.roles &&
          currentUser.roles.map((role, index) => <li key={index}>{role}</li>)}
      </ul> */}

      {/* Bootstrap 4.6 Modal */}
      <div
        className={`modal fade ${showModal ? "show d-block" : ""}`}
        tabIndex="-1"
        role="dialog"
        style={{ background: "rgba(0, 0, 0, 0.5)" }}
      >
        <div className="modal-dialog" role="document">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Session Expired</h5>
            </div>
            <div className="modal-body">
              Your access token has expired. Still you want to logged In?
            </div>
            <div className="modal-footer">
              <button className="btn btn-danger" onClick={handleLogout}>
                Logout
              </button>
              <button className="btn btn-primary" onClick={handleRefreshToken}>
                Continue
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Force Bootstrap modal to close on backdrop click */}
      {showModal && (
        <div
          className="modal-backdrop fade show"
          onClick={() => setShowModal(false)}
        ></div>
      )}
    </div>
  );
};

export default Profile;
