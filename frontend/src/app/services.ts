export const fetchImageData = async (searchTerm: string = '', page: number = 1, pageSize: number = 10) => {
  const response = await fetch(`http://localhost:9000/data?search=${searchTerm}&page=${page}&page_size=${pageSize}`);
  return response.json();
};
