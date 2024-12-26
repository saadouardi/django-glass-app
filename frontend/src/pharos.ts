import registerComponents from "@ithaka/pharos/lib/utils/registerComponents";
import {
  PharosButton,
  PharosHeading,
  PharosIcon,
  PharosImageCard,
  PharosModal,
} from "@ithaka/pharos";

import "@ithaka/pharos/lib/styles/fonts.css";
import "@ithaka/pharos/lib/styles/typography.scss";
import "@ithaka/pharos/lib/styles/_variables.scss";
import "@ithaka/pharos/lib/styles/variables.css";

registerComponents("image-gallery", [
  PharosButton,
  PharosHeading,
  PharosImageCard,
  PharosModal,
  PharosIcon,
]);
