---
description: "Task list for creating a Docusaurus book on Physical AI and Humanoid Robotics"
---

# Tasks: Physical AI and Humanoid Robotics Textbook

**Input**: User specification for a Docusaurus book.  
**Prerequisites**: A Docusaurus project is expected to be set up.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel  
- **[Story]**: Which user story (chapter section) this task belongs to (e.g., FND1, ROS2-2, SIM1)
- Include **exact file paths** in descriptions.


# Phase 1: Setup (Docusaurus Project Initialization)

- [x] T001 Initialize Docusaurus project `physical-ai-book`
- [x] T002 Configure `docusaurus.config.ts` (title, author, repo)
- [x] T003 [P] Add logo + favicon → `frontend/static/img/`
- [x] T004 [P] Customize theme → `frontend/src/css/custom.css`


# Phase 2: Book Structure (Matches Your File Tree)

## Purpose  
Ensure folder structure and sidebar navigation exist.

- [ ] T005 Create main intro page → `frontend/docs/intro.md`
- [ ] T006 [P] Build sidebar nav in `frontend/sidebars.ts` using **01–05** chapter folders
- [ ] T007 [P] Verify placeholder `_index.mdx` exists in all chapters:

    ```

    frontend/docs/01-foundations/_index.mdx
    frontend/docs/02-ros2/_index.mdx
    frontend/docs/03-simulation/_index.mdx
    frontend/docs/04-isaac/_index.mdx
    frontend/docs/05-humanoid/_index.mdx

    ```



# Phase 3  
# **User Story: 01 Foundations**  
Folder: `frontend/docs/01-foundations/`

This story includes 4 files:

- `1-1-embodied-intelligence.mdx`
- `1-2-real-time.mdx`
- `1-3-perception-systems.mdx`
- `1-4-internal-sensors.mdx`

### Tasks

- [ ] T008 [FND1] Write: Embodied Intelligence  
  → `frontend/docs/01-foundations/1-1-embodied-intelligence.mdx`

- [ ] T009 [FND2] Write: Real-Time Systems  
  → `frontend/docs/01-foundations/1-2-real-time.mdx`

- [ ] T010 [FND3] Write: Perception Systems  
  → `frontend/docs/01-foundations/1-3-perception-systems.mdx`

- [ ] T011 [FND4] Write: Internal Sensors  
  → `frontend/docs/01-foundations/1-4-internal-sensors.mdx`

---

# Phase 4  
# **User Story: 02 ROS2**  
Folder: `frontend/docs/02-ros2/`

Files:

- `2-1-ros2-architecture.mdx`
- `2-2-rclpy-packages.mdx`
- `2-3-urdf-kinematics.mdx`

### Tasks

- [ ] T012 [ROS2-1] Write ROS2 Architecture  
  → `frontend/docs/02-ros2/2-1-ros2-architecture.mdx`

- [ ] T013 [ROS2-2] Write rclpy Packages  
  → `frontend/docs/02-ros2/2-2-rclpy-packages.mdx`

- [ ] T014 [ROS2-3] Write URDF & Kinematics  
  → `frontend/docs/02-ros2/2-3-urdf-kinematics.mdx`

---

# Phase 5  
# **User Story: 03 Simulation**  
Folder: `frontend/docs/03-simulation/`

Files:

- `3-1-gazebo-physics.mdx`
- `3-2-unity-visualization.mdx`

### Tasks

- [ ] T015 [SIM1] Write Gazebo Physics  
  → `frontend/docs/03-simulation/3-1-gazebo-physics.mdx`

- [ ] T016 [SIM2] Write Unity Visualization  
  → `frontend/docs/03-simulation/3-2-unity-visualization.mdx`

---

# Phase 6  
# **User Story: 04 Isaac**  
Folder: `frontend/docs/04-isaac/`

Files:

- `4-1-isaac-sim-data.mdx`
- `4-2-vslam-pipelines.mdx`

### Tasks

- [ ] T017 [ISAAC1] Write: Isaac Sim Data  
  → `frontend/docs/04-isaac/4-1-isaac-sim-data.mdx`

- [ ] T018 [ISAAC2] Write: VSLAM Pipelines  
  → `frontend/docs/04-isaac/4-2-vslam-pipelines.mdx`


# Phase 7  
# **User Story: 05 Humanoid Robotics**  
Folder: `frontend/docs/05-humanoid/`

Files:

- `5-1-locomotion-balance.mdx`
- `5-2-manipulation-grasping.mdx`
- `5-3-vla-cognitive.mdx`

### Tasks

- [ ] T019 [HUM1] Write Locomotion & Balance  
  → `frontend/docs/05-humanoid/5-1-locomotion-balance.mdx`

- [ ] T020 [HUM2] Write Manipulation & Grasping  
  → `frontend/docs/05-humanoid/5-2-manipulation-grasping.mdx`

- [ ] T021 [HUM3] Write VLA & Cognitive Models  
  → `frontend/docs/05-humanoid/5-3-vla-cognitive.mdx`


# Phase 8: Polish & Cross-Cutting Tasks

- [ ] T022 [P] Edit/Review all `.mdx` files
- [ ] T023 [P] Add diagrams/images  
  → Add to: `frontend/assets/diagrams/` or `frontend/assets/images/`
- [ ] T024 Build the Docusaurus site and fix errors
- [ ] T025 Deploy (GitHub Pages / Cloudflare / Netlify)



## Dependencies & Execution Order

### Phase Dependencies

* **Setup (Phase 1)**
  Can start immediately.

* **Book Structure (Phase 2)**
  Depends on Setup completion (folders, sidebar, intro page).

* **Chapter Development (Phases 3–7)**
  Each chapter (01–05) depends on Phase 2 completion.

  Chapters include:

  * **Phase 3: 01 Foundations**
  * **Phase 4: 02 ROS2**
  * **Phase 5: 03 Simulation**
  * **Phase 6: 04 Isaac**
  * **Phase 7: 05 Humanoid**

* **Polish (Phase 8)**
  Depends on all content chapters (Phases 3–7) being complete.


### User Story Dependencies

* All **five chapters (01–05)** can be written **in parallel** once the foundational structure (Phase 2) is complete.
* No chapter depends on another (e.g., ROS2 does not depend on Simulation).
* Editing & media tasks can overlap with writing, but final polish requires all chapters to exist.

### Parallel Opportunities

* **Fully parallel writing** across chapters:

  * Foundations tasks (T008–T011)
  * ROS2 tasks (T012–T014)
  * Simulation tasks (T015–T016)
  * Isaac tasks (T017–T018)
  * Humanoid tasks (T019–T021)

* **Polish tasks** (T022–T023)
  Can run parallel while content is developed, as long as they don’t block content creation.

* **Deployment (T024–T025)**
  Must occur after a stable build of the entire book.

---

## Implementation Strategy 

### MVP First (Chapter 01: Foundations)

1. **Complete Phase 1: Setup**
2. **Complete Phase 2: Book structure** (sidebar, intro.md, folder validation)
3. **Complete Phase 3: Foundations chapter**

   * `1-1-embodied-intelligence.mdx`
   * `1-2-real-time.mdx`
   * `1-3-perception-systems.mdx`
   * `1-4-internal-sensors.mdx`
4. **STOP and VALIDATE**:

   * Foundations chapter builds
   * Navigation works
   * Styling + structure look correct

**This becomes your MVP release.**

### Incremental Delivery (Chapter-by-Chapter Releases)

1. Setup + Structure (Phases 1–2)
2. Add **Chapter 01 – Foundations** → Deploy
3. Add **Chapter 02 – ROS2** → Deploy
4. Add **Chapter 03 – Simulation** → Deploy
5. Add **Chapter 04 – Isaac** → Deploy
6. Add **Chapter 05 – Humanoid** → Deploy
7. Run Polish Phase (media, editing) → Final Deploy