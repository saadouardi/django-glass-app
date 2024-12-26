interface ImagePermissions {
  permcomment: number;
}

interface Image {
  id: string;
  owner: string;
  secret: string;
  server: string;
  farm: number;
  title: string;
  ispublic: number;
  isfriend: number;
  isfamily: number;
  safe: number;
  license: string;
  needs_interstitial: number;
  description: string;
  rotation: number;
  ownername: string;
  count_faves: string;
  count_comments: string;
  can_comment: number;
  permissions: ImagePermissions;
  media: string;
  media_status: string;
  url_l?: string;
  url_l_cdn?: string;
  height_l?: string;
  width_l?: string;
  url_m: string;
  url_m_cdn: string;
  height_m: string | number;
  width_m: string | number;
  url_n?: string;
  url_n_cdn?: string;
  height_n?: string | number;
  width_n?: string | number;
  url_q: string;
  url_q_cdn: string;
  height_q: string | number;
  width_q: string | number;
  url_s: string;
  url_s_cdn: string;
  height_s: string | number;
  width_s: string | number;
  url_sq: string;
  url_sq_cdn: string;
  height_sq: string | number;
  width_sq: string | number;
  url_t: string;
  url_t_cdn: string;
  height_t: string | number;
  width_t: string | number;
  url_z?: string;
  url_z_cdn?: string;
  height_z?: string | number;
  width_z?: string | number;
  pathalias: string | null;
}

export type ImageState = {
  images: Array<Image>;
  currentImageId?: string;
};

export type iStateAction = {
  type: string;
  payload: any;
};

export const initialState: ImageState = {
  images: [],
  currentImageId: undefined,
};

export const ImageReducer = (state = initialState, action: any): ImageState => {
  switch (action.type) {
    case "SetImages":
      return {
        ...state,
        images: action.payload,
      };
    case "SetCurrentImage":
      return {
        ...state,
        currentImageId: action.payload,
      };
    default:
      return state;
  }
};
