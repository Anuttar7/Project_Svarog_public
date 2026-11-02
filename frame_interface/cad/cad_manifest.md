# CAD File Manifest: Frame Interface

| File | Format | Description | Source |
|---|---|---|---|
| `atrium_1u_reference.step` | ISO 10303-21 STEP AP214 | Complete 3D solid geometry of the Svarog 1U reference structural chassis, including rails, corner pads, open ring flanges, and X-braces. | `icss-briefs/drafts/svarog-1u-reference/` |
| `frame_geometry.py` | Python (Fusion 360 API) | Parametric geometry generator defining rails, pads, rings, and braces using Fusion 360 `TemporaryBRepManager`. | `icss-briefs/drafts/svarog-1u-reference/` |

### Key Parameters in `frame_geometry.py`:
- `cube`: 100.0 mm
- `leg`: 8.5 mm (rail leg width)
- `t_rail`: 1.6 mm (rail thickness)
- `pad`: 6.0 mm (contact pad size)
- `pad_h`: 3.0 mm (contact pad height)
- `ring_w`: 6.0 mm (ring face width)
- `ring_t`: 1.6 mm (ring face thickness)
- `brace_w`: 3.0 mm (strut brace width)
- `brace_t`: 1.6 mm (strut brace thickness)
- `gus_leg`: 18.0 mm (gusset leg length)
