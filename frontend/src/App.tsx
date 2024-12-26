import {
  PharosButton,
  PharosImageCard,
  PharosModal
} from "@ithaka/pharos/lib/react-components";

import { MouseEvent, useReducer, useEffect, useState } from "react";
import { ImageReducer, initialState } from "./app/reducer";
import ImagesContext from "./app/context";
import { fetchImageData } from "./app/services";
import DefaultImage from "../src/assets/images/default-image.png";

function App() {
  const [imageState, imageStateDispatch] = useReducer(
    ImageReducer,
    initialState
  );
  const currentImage = imageState.images.find(
    (image) => image.id === imageState.currentImageId
  );

  // States for Pagination and Search
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredImages, setFilteredImages] = useState(imageState.images);

  // States for Modal Form
  const [updatedTitle, setUpdatedTitle] = useState(currentImage?.title || "");
  const [updatedDescription, setUpdatedDescription] = useState(currentImage?.description || "");
  const [updatedIsPublic, setUpdatedIsPublic] = useState(currentImage?.ispublic === 1);

  // State to control modal visibility
  const [isModalOpen, setIsModalOpen] = useState(false);

  const itemsPerPage = 10;

  // Calculate the starting and ending indices for the current page
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;

  // Slice the images to display only the current page's images
  const currentImages = filteredImages.slice(startIndex, endIndex);

  useEffect(() => {
    fetchImageData().then((data) => {
      imageStateDispatch({ type: "SetImages", payload: data });
      setFilteredImages(data);
    });
  }, []);

  useEffect(() => {
    if (searchTerm.trim() === "") {
      setFilteredImages(imageState.images);
    } else {
      setFilteredImages(
        imageState.images.filter((image) =>
          image.title.toLowerCase().includes(searchTerm.toLowerCase())
        )
      );
      setCurrentPage(1);
    }
  
    // Close the modal if the current image is no longer part of the filtered images
    if (currentImage && !filteredImages.find(image => image.id === currentImage.id)) {
      setIsModalOpen(false);
    }
  
  }, [searchTerm, imageState.images, currentImage, filteredImages]);
  

  // When a new image is clicked, update the form state
  useEffect(() => {
    if (currentImage) {
      setUpdatedTitle(currentImage.title);
      setUpdatedDescription(currentImage.description);
      setUpdatedIsPublic(currentImage.ispublic === 1);
    }
  }, [currentImage]);

  const onImageClick = async (e: MouseEvent, imageId: string) => {
    e.preventDefault();
    await imageStateDispatch({ type: "SetCurrentImage", payload: imageId });
    setIsModalOpen(true); // Open the modal when an image is clicked
  };

  // Handle Next Page
  const nextPage = () => {
    if (currentPage * itemsPerPage < filteredImages.length) {
      setCurrentPage(currentPage + 1);
    }
  };

  // Handle Previous Page
  const prevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  // Handle image URL error and show default image
  const handleImageError = (
    e: React.SyntheticEvent<HTMLImageElement, Event>
  ) => {
    e.currentTarget.src = DefaultImage;
  };

  const handleSave = async () => {
    if (!currentImage) {
      console.error("No image selected.");
      return;
    }

    const updatedImage = {
      id: currentImage.id,
      title: updatedTitle,
      description: updatedDescription,
      ispublic: updatedIsPublic ? 1 : 0,
      url_m_cdn: currentImage.url_m_cdn
    };

    const response = await fetch(`http://localhost:9000/update/${currentImage.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(updatedImage)
    });

    if (response.ok) {
      // Update image in state
      imageStateDispatch({ type: "SetImages", payload: imageState.images.map(img => img.id === updatedImage.id ? updatedImage : img) });
      // Close modal
      setIsModalOpen(false);
    } else {
      console.error("Failed to save changes");
    }
  };

  return (
    <ImagesContext.Provider value={{ imageState, imageStateDispatch }}>
      <div className="image-gallery">
        <h1 className="image-gallery__heading text-primary">Image Gallery</h1>

        {/* Search Bar */}
        <div className="search d-flex align-items-center justify-content-center gap-2">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="form-control w-50"
            placeholder="Search by title"
          />
          <button
            className="btn btn-danger"
            onClick={() => setSearchTerm("")}
          >
            Clear
          </button>
        </div>

        {/* Display Images */}
        <div className="image-grid">
          {currentImages.length > 0 ? (
            currentImages.map((image) => (
              <PharosImageCard
                title={image.title}
                key={image.id}
                onClick={(e) => onImageClick(e, image.id)}
                className="gallery-container bg-light"
              >
                <img
                  slot="image"
                  src={image.url_m_cdn ? image.url_m_cdn : DefaultImage}
                  alt={`An image titled "${image.title}" by ${image.ownername}`}
                  className="gallery-image"
                  onError={handleImageError}
                />
                <div slot="metadata">By {image.ownername}</div>
              </PharosImageCard>
            ))
          ) : (
            <div className="text-warning">No images found matching your search term.</div>
          )}
        </div>

        {/* Pagination Controls */}
        <div className="pagination-controls d-flex align-items-center justify-content-center gap-2">
          <button
            type="button" 
            onClick={prevPage} 
            disabled={currentPage === 1}
            className="btn btn-primary"
          >
            {}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              className="bi bi-arrow-left-short"
              viewBox="0 0 16 16"
            >
              <path
                fillRule="evenodd"
                d="M12 8a.5.5 0 0 1-.5.5H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5H11.5a.5.5 0 0 1 .5.5"
              />
            </svg>
          </button>
          <span className="pagination-info text-primary">
            Page {currentPage} of{" "}
            {Math.ceil(filteredImages.length / itemsPerPage)}
          </span>
          <button
            type="button"
            onClick={nextPage}
            disabled={currentPage * itemsPerPage >= filteredImages.length}
            className="btn btn-primary"
          >
            {}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              className="bi bi-arrow-right-short"
              viewBox="0 0 16 16"
            >
              <path
                fillRule="evenodd"
                d="M4 8a.5.5 0 0 1 .5-.5h5.793L8.146 5.354a.5.5 0 1 1 .708-.708l3 3a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708-.708L10.293 8.5H4.5A.5.5 0 0 1 4 8"
              />
            </svg>
          </button>
        </div>

        {/* Modal */}
        <PharosModal id="image-modal" header={updatedTitle} open={isModalOpen}>
          <hr />
          <div>
            {currentImage && (
              <div className="form d-flex flex-column gap-2">
                <input
                  type="text"
                  value={updatedTitle}
                  onChange={(e) => setUpdatedTitle(e.target.value)}
                  placeholder="Title"
                />
                <textarea
                  value={updatedDescription}
                  onChange={(e) => setUpdatedDescription(e.target.value)}
                  placeholder="Description"
                />
                <label className="d-flex align-items-center justify-content-start gap-2">
                  Public domain{" "}
                  <input
                    type="checkbox"
                    checked={updatedIsPublic}
                    onChange={() => setUpdatedIsPublic(!updatedIsPublic)}
                  />
                </label>
                <label>
                  ID: <span>{currentImage.id}</span>
                </label>
                <label>
                  Owner Name: <span>{currentImage.ownername}</span>
                </label>
                <label>
                  Image Dimension: {currentImage.width_m} x{" "}
                  {currentImage.height_m}
                </label>
              </div>
            )}
          </div>
          <hr />
          <div className="d-flex justify-content-end gap-2">
            <PharosButton
              slot="footer"
              type="button"
              variant="secondary"
              onClick={() => setIsModalOpen(false)}
            >
              Cancel
            </PharosButton>
            <PharosButton slot="footer" type="button" onClick={handleSave}>
              Save
            </PharosButton>
          </div>
        </PharosModal>
      </div>
    </ImagesContext.Provider>
  );
}

export default App;
