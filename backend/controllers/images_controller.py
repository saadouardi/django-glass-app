from services.images import get_images as service_get_images, update_image as service_update_image

def get_images(search=None, page=1, page_size=10):
    """Retrieve images."""
    return service_get_images(search, page, page_size)

def update_image(image_id, image):
    """Update an image."""
    return service_update_image(image_id, image)
