import pygame

class ImageCache:
    def __init__(self):
        self.loaded_images = {}

    def get_image(self, path, scale=None):
        key = (path, tuple(scale)) if scale else path
        if key not in self.loaded_images:
            try:
                image = pygame.image.load(path).convert_alpha()
                if scale:
                    image = pygame.transform.scale(image, scale)
                self.loaded_images[key] = image
                print(f"Loaded {path} into cache.")
            except Exception as e:
                print(f"Failed to load image {path}: {str(e)}")
                return None
        return self.loaded_images[key]