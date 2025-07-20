# 🎓 SkillShare Hub – Django Web Application

A micro-learning platform built with Django where users can register as **students** or **instructors**, create and enroll in courses, leave feedback, and manage profiles — developed as part of the Django Advanced Course @ SoftUni.

---

## 🚀 Features

### 🔐 Authentication & User Roles
- Custom **registration** form with email
- Django **login/logout** system with custom templates
- Role-based access: `student` or `instructor`
- **Dashboard redirect** after login based on role
- Profile editing: bio, avatar, and role
- Role-based access enforcement (e.g., only instructors can create courses)

### 🎓 Learning System
- Instructors can:
  - Create/edit/delete **courses**
  - Upload **videos and lessons**
- Students can:
  - **Enroll** in courses
  - View their **enrolled content**
- All users can view public course listings

### 💬 Feedback System
- Students can rate and review courses
- Instructors can see feedback on their courses

### ⚙ Admin Panel
- Extended Django Admin with:
  - Custom list display, filters, and search
  - Role-based permission groups (superuser & staff)
  - Manage user roles and models from admin

### 🎨 UI/UX
- Bootstrap 5-based responsive design
- Custom `base.html` with navbar and layout
- Flash messages for actions (login, register, update, etc.)

### 🌐 Project Structure
Modular Django apps:
- `users` – authentication, profile, roles
- `courses` – course and lesson models
- `enrollments` – track user-course relationships
- `feedback` – user ratings and comments
- `api` *(optional)* – RESTful endpoints

---

## 📂 Directory Structure (Main Apps)

