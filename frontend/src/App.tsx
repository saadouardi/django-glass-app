import React, { useReducer, useEffect, useState } from "react";
import {
  PharosButton,
  PharosImageCard,
  PharosModal
} from "@ithaka/pharos/lib/react-components";
import { ImageReducer, initialState } from "./app/reducer";
import ImagesContext from "./app/context";
import { fetchImageData } from "./app/services";
import DefaultImage from "../src/assets/images/default-image.png";

function App() {
  const [imageState, imageStateDispatch] = useReducer(
    ImageReducer,
    initialState
  );
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [updatedTitle, setUpdatedTitle] = useState("");
  const [updatedDescription, setUpdatedDescription] = useState("");
  const [updatedIsPublic, setUpdatedIsPublic] = useState(false);
  const itemsPerPage = 10;
  const isLastPage = currentPage * itemsPerPage >= totalPages;

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchImageData(searchTerm, currentPage, 10);
      if (data.images && data.total) {
        imageStateDispatch({ type: "SetImages", payload: data.images });
        setTotalPages(Math.ceil(data.total / 10));
      }
    };
    fetchData();
  }, [searchTerm, currentPage]);

  const onImageClick = (e: React.MouseEvent<HTMLElement>, imageId: string) => {
    e.preventDefault();
    imageStateDispatch({ type: "SetCurrentImage", payload: imageId });
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
      ispublic: updatedIsPublic ? 1 : 0
    };

    const response = await fetch(
      `http://localhost:9000/update/${currentImage.id}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(updatedImage)
      }
    );

    if (response.ok) {
      imageStateDispatch({
        type: "SetImages",
        payload: imageState.images.map((img) =>
          img.id === updatedImage.id ? updatedImage : img
        )
      });
      setIsModalOpen(false);
    } else {
      console.error("Failed to save changes");
    }
  };
  
  const currentImage = imageState.images.find(
    (image) => image.id === imageState.currentImageId
  );
  useEffect(() => {
    if (currentImage) {
      setUpdatedTitle(currentImage.title);
      setUpdatedDescription(currentImage.description);
      setUpdatedIsPublic(currentImage.ispublic === 1);
      setIsModalOpen(true);
    }
  }, [currentImage]);

  return (
    <ImagesContext.Provider value={{ imageState, imageStateDispatch }}>
      <div className="image-gallery">
        <h1 className="image-gallery__heading text-primary">Image Gallery</h1>
        
        <div className="search d-flex align-items-center justify-content-center gap-2">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="form-control w-50"
            placeholder="Search by title"
          />
          <button className="btn btn-danger" onClick={() => setSearchTerm("")}>
            Clear
          </button>
        </div>

        <div className="image-grid">
          {imageState.images.length ? (
            imageState.images.map((image) => (
              <PharosImageCard
                title={image.title}
                key={image.id}
                onClick={(e) => onImageClick(e, image.id)}
                className="gallery-container bg-light"
              >
                <img
                  slot="image"
                  src={image.url_m_cdn || DefaultImage}
                  alt={`An image titled "${image.title}"`}
                  className="gallery-image"
                  onError={(e) => (e.currentTarget.src = DefaultImage)}
                />
                <div slot="metadata">
                  {image.description.length > 0 ? image.description.length > 16 ? 'Description: ' + image.description.slice(0, 16) + '...' : 'Description: ' + image.description
                  : (<div className="text-danger">No description available</div>)}
                </div>
                <div slot="metadata">By {image.ownername}</div>
              </PharosImageCard>
            ))
          ) : (
            <div className="text-warning">
              No images found matching your search term.
            </div>
          )}
        </div>

        <div className="pagination-controls d-flex align-items-center justify-content-center gap-2">
          <button
            disabled={currentPage === 1}
            onClick={() => setCurrentPage(currentPage - 1)}
            className="btn btn-primary"
          >
            Previous
          </button>
          <span className="text-light">
            Page {currentPage} of {totalPages}
          </span>
          <button
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage(currentPage + 1)}
            className="btn btn-primary"
          >
            Next
          </button>
        </div>
        
        {currentImage && (
          <PharosModal
            id="image-modal"
            header={updatedTitle}
            open={isModalOpen}
          >
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
        )}
      </div>
    </ImagesContext.Provider>
  );
}

export default App;
