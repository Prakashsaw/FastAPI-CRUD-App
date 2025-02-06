import axios from "axios";
import { BASE_URL } from "../utils/baseurl.util";

const API_URL = `${BASE_URL}/api/v1/user`;

const register = (name, email, password) => {
  return axios.post(`${API_URL}/signup`, {
    name,
    email,
    password,
  });
};

const verifyAccount = (token, email) => {
  return axios.post(
    `${API_URL}/user-account-verification/${token}/${email}`,
    {}
  );
};

const login = async (email, password) => {
  return await axios
    .post(`${API_URL}/login`, {
      email,
      password,
    })
    .then((response) => {
      if (response.data.user) {
        localStorage.setItem("user", JSON.stringify(response.data));
      }

      return response.data;
    });
};

const sendResetPasswordLink = (email) => {
  return axios.post(`${API_URL}/send-password-reset-link`, {
    email,
  });
};

const resetPassword = (token, password) => {
  return axios.post(`${API_URL}/reset-password/${token}`, {
    password,
  });
};

const getCurrentUser = () => {
  return JSON.parse(localStorage.getItem("user"));
};

const isTokenExpired = (token) => {
  if (!token) return true;
  const payload = JSON.parse(atob(token.split(".")[1]));
  console.log("payload", payload);
  console.log("Date.now()", Date.now());
  console.log("payload.exp * 1000", payload.exp * 1000);
  return payload.exp * 1000 < Date.now();
};

const refreshToken = async () => {
  try {
    const user = getCurrentUser();
    const jwt_refresh_token = user.jwt_refresh_token;
    const response = await axios.post(
      `${API_URL}/renew-access-token`,
      {},
      {
        headers: {
          Authorization: `Bearer ${jwt_refresh_token}`,
        },
      }
    );
    const newUser = {
      ...user,
      jwt_access_token: response.data.jwt_access_token,
    };
    localStorage.setItem("user", JSON.stringify(newUser));
    return newUser;
  } catch (error) {
    console.error("Error refreshing token", error);
    throw error;
  }
};

const logout = async () => {
  localStorage.removeItem("user");
  return await axios.post(`${API_URL}/logout`).then((response) => {
    return response.data;
  });
};

const AuthService = {
  register,
  verifyAccount,
  login,
  sendResetPasswordLink,
  resetPassword,
  getCurrentUser,
  isTokenExpired,
  refreshToken,
  logout,
};

export default AuthService;
