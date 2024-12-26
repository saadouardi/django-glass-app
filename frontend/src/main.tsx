import React from "react";
import ReactDOM from "react-dom/client";
import { PharosContext } from "@ithaka/pharos/lib/utils/PharosContext";

import App from "./App";
import "./index.scss";
import "./pharos";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <PharosContext.Provider value={{ prefix: "image-gallery" }}>
      <App />
    </PharosContext.Provider>
  </React.StrictMode>,
);
