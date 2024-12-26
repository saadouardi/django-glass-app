export const fetchImageData = async () => {
  return fetch("http://localhost:9000/data")
    .then((response) => response.json())
    .then((data) => data);
};
