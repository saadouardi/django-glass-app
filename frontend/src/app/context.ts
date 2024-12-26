import { Dispatch, createContext } from "react";
import { ImageState, initialState, iStateAction } from "./reducer";

const ImagesContext = createContext<{
  imageState: ImageState;
  imageStateDispatch: Dispatch<iStateAction>;
}>({
  imageState: initialState,
  imageStateDispatch: () => null,
});

export default ImagesContext;
