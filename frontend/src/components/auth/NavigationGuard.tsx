// frontend/src/components/auth/NavigationGuard.tsx
import { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

export const NavigationGuard: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    // Define public routes that don't require authentication
    const publicRoutes = ['/login', '/signup', '/forgot-password'];
    const isPublicRoute = publicRoutes.some(route =>
      location.pathname === route || location.pathname.startsWith(`${route}/`)
    );

    // If user is authenticated and on a public route, redirect to dashboard
    if (isAuthenticated && isPublicRoute) {
      navigate('/dashboard', { replace: true });
    }
    // If user is not authenticated and not on a public route, redirect to login
    else if (!isAuthenticated && !isPublicRoute && !isLoading) {
      navigate('/login', { replace: true });
    }
  }, [isAuthenticated, isLoading, location.pathname, navigate]);

  return null; // This component doesn't render anything
};