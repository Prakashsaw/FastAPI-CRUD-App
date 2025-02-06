import axios from "axios";

// const API_URL = `${BASE_URL}/api/v1/book`;
const API_URL = "http://localhost:5000/api/v1/user";

const getPublicContent = () => {
  return axios.get(API_URL + "/all-books");
};

const getUserBoard = () => {
  return axios.get(API_URL + "/user");
};

const getModeratorBoard = () => {
  return axios.get(API_URL + "/mod");
};

const getAdminBoard = () => {
  return axios.get(API_URL + "/admin");
};

const UserService = {
  getPublicContent,
  getUserBoard,
  getModeratorBoard,
  getAdminBoard,
};

export default UserService;
