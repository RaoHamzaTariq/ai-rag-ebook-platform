// frontend/src/utils/tokenStorage.ts

// Store token in localStorage
export const storeToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('authToken', token);
  }
};

// Get token from localStorage
export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('authToken');
  }
  return null;
};

// Remove token from localStorage
export const removeToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('authToken');
  }
};

// Store user info in localStorage
export const storeUserInfo = (userInfo: any): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('userInfo', JSON.stringify(userInfo));
  }
};

// Get user info from localStorage
export const getUserInfo = (): any => {
  if (typeof window !== 'undefined') {
    const userInfo = localStorage.getItem('userInfo');
    return userInfo ? JSON.parse(userInfo) : null;
  }
  return null;
};

// Remove user info from localStorage
export const removeUserInfo = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('userInfo');
  }
};

// Clear all auth-related data from localStorage
export const clearAuthData = (): void => {
  removeToken();
  removeUserInfo();
};