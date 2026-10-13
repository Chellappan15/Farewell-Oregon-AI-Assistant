import React, { useState, useEffect } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import {
  ShieldAlert,
  Lock,
  Mail,
  User as UserIcon,
  Eye,
  EyeOff,
  ArrowRight,
  Loader2,
  Radio,
  Gamepad2,
  CheckCircle2,
  AlertCircle,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";

export const AuthPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated, login, register } = useAuth();

  const isRegisterRoute = location.pathname.includes("/register");
  const [isRegister, setIsRegister] = useState(isRegisterRoute);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const [submitting, setSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Sync state if URL route changes
  useEffect(() => {
    setIsRegister(location.pathname.includes("/register"));
    setErrorMessage(null);
  }, [location.pathname]);

  // If already logged in, redirect to destination or home
  useEffect(() => {
    if (isAuthenticated) {
      const from = (location.state as { from?: { pathname?: string } })?.from?.pathname || "/";
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, location]);

  const validateForm = (): boolean => {
    setErrorMessage(null);
    const trimmedEmail = email.trim().toLowerCase();

    if (!trimmedEmail) {
      setErrorMessage("Please enter your callsign / email address.");
      return false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(trimmedEmail)) {
      setErrorMessage("Please enter a valid email format (e.g. deacon@farewell.org).");
      return false;
    }

    if (!password) {
      setErrorMessage("Please enter your security passcode.");
      return false;
    }

    if (password.length < 6) {
      setErrorMessage("Security passcode must be at least 6 characters long.");
      return false;
    }

    if (isRegister) {
      if (password !== confirmPassword) {
        setErrorMessage("Passcodes do not match. Please verify and re-enter.");
        return false;
      }
    }

    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setSubmitting(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      if (isRegister) {
        await register({
          email: email.trim().toLowerCase(),
          password,
          name: name.trim() || undefined,
        });
        setSuccessMessage("Clearance verified. Welcome to the Wilderness Archive.");
      } else {
        await login({
          email: email.trim().toLowerCase(),
          password,
        });
        setSuccessMessage("Access granted. Initializing tactical feed...");
      }

      // Navigate will trigger via useEffect once isAuthenticated updates
      const from = (location.state as { from?: { pathname?: string } })?.from?.pathname || "/";
      navigate(from, { replace: true });
    } catch (err: unknown) {
      let message = "Authentication failed. Please check your credentials.";
      if (err && typeof err === "object") {
        const axErr = err as { response?: { data?: { detail?: string; message?: string } }; message?: string };
        if (axErr.response?.data?.detail) {
          message = axErr.response.data.detail;
        } else if (axErr.response?.data?.message) {
          message = axErr.response.data.message;
        } else if (axErr.message) {
          message = axErr.message;
        }
      }
      setErrorMessage(message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page-container">
      {/* Background ambient lighting */}
      <div className="auth-ambient-glow-amber" />
      <div className="auth-ambient-glow-red" />

      {/* Main Terminal Card */}
      <div className="auth-card">
        {/* Tactical Header Badge */}
        <div className="auth-header">
          <div className="auth-brand">
            <div className="auth-brand-icon">
              <Gamepad2 size={20} />
            </div>
            <div>
              <h1 className="auth-brand-title">DAYS GONE // ARCHIVE</h1>
              <p className="auth-brand-subtitle">NERO SECURE TERMINAL • V2.4</p>
            </div>
          </div>
          <div className="auth-status-badge">
            <Radio size={12} className="auth-status-dot" />
            <span>ONLINE</span>
          </div>
        </div>

        {/* Tab Switcher */}
        <div className="auth-tabs">
          <button
            type="button"
            className={`auth-tab-btn ${!isRegister ? "active" : ""}`}
            onClick={() => {
              setIsRegister(false);
              navigate("/login");
            }}
          >
            SURVIVOR LOGIN
          </button>
          <button
            type="button"
            className={`auth-tab-btn ${isRegister ? "active" : ""}`}
            onClick={() => {
              setIsRegister(true);
              navigate("/register");
            }}
          >
            NEW DRIFTER
          </button>
        </div>

        {/* Heading */}
        <div className="auth-heading-group">
          <h2 className="auth-heading">
            {isRegister ? "Enroll Survivor Clearance" : "Authorize Terminal Access"}
          </h2>
          <p className="auth-subheading">
            {isRegister
              ? "Register your callsign to track hordes, weapon caches, and tactical lore."
              : "Enter your registered callsign and passcode to decrypt tactical intel."}
          </p>
        </div>

        {/* Error Alert */}
        {errorMessage && (
          <div className="auth-alert auth-alert-error animate-fadeIn">
            <AlertCircle size={16} className="auth-alert-error-icon" />
            <span>{errorMessage}</span>
          </div>
        )}

        {/* Success Alert */}
        {successMessage && (
          <div className="auth-alert auth-alert-success animate-fadeIn">
            <CheckCircle2 size={16} className="auth-alert-success-icon" />
            <span>{successMessage}</span>
          </div>
        )}

        {/* Auth Form */}
        <form onSubmit={handleSubmit} className="auth-form">
          {/* Name Field (Register only) */}
          {isRegister && (
            <div className="auth-field">
              <label className="auth-label">
                Survivor Alias / Name <span className="auth-optional">(Optional)</span>
              </label>
              <div className="auth-input-wrapper">
                <div className="auth-input-prefix-icon">
                  <UserIcon size={16} />
                </div>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Deacon St. John"
                  className="auth-input"
                />
              </div>
            </div>
          )}

          {/* Email Field */}
          <div className="auth-field">
            <label className="auth-label">
              Callsign / Email Address <span className="auth-required">*</span>
            </label>
            <div className="auth-input-wrapper">
              <div className="auth-input-prefix-icon">
                <Mail size={16} />
              </div>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="deacon@farewell.org"
                className="auth-input"
              />
            </div>
          </div>

          {/* Password Field */}
          <div className="auth-field">
            <label className="auth-label">
              Security Passcode <span className="auth-required">*</span>
            </label>
            <div className="auth-input-wrapper">
              <div className="auth-input-prefix-icon">
                <Lock size={16} />
              </div>
              <input
                type={showPassword ? "text" : "password"}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="auth-input"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="auth-password-toggle"
                tabIndex={-1}
              >
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
            <p className="auth-field-hint">
              Minimum 6 characters • Encrypted with bcrypt
            </p>
          </div>

          {/* Confirm Password (Register only) */}
          {isRegister && (
            <div className="auth-field">
              <label className="auth-label">
                Verify Passcode <span className="auth-required">*</span>
              </label>
              <div className="auth-input-wrapper">
                <div className="auth-input-prefix-icon">
                  <ShieldAlert size={16} />
                </div>
                <input
                  type={showPassword ? "text" : "password"}
                  required
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="••••••••••••"
                  className="auth-input"
                />
              </div>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={submitting}
            className="auth-submit-btn"
          >
            {submitting ? (
              <>
                <Loader2 size={16} className="auth-submit-spinner" />
                <span>{isRegister ? "ENROLLING SURVIVOR..." : "VERIFYING CLEARANCE..."}</span>
              </>
            ) : (
              <>
                <span>{isRegister ? "ENROLL IN ARCHIVE" : "ACCESS ARCHIVE"}</span>
                <ArrowRight size={15} />
              </>
            )}
          </button>
        </form>

        {/* Bottom Link */}
        <div className="auth-card-footer">
          {isRegister ? (
            <p className="auth-footer-prompt">
              Already have an archive callsign?
              <Link to="/login" className="auth-footer-link">
                Sign in here
              </Link>
            </p>
          ) : (
            <p className="auth-footer-prompt">
              Need drifter clearance in Oregon?
              <Link to="/register" className="auth-footer-link">
                Enroll as new drifter
              </Link>
            </p>
          )}
        </div>
      </div>

      {/* Footer watermark */}
      <div className="auth-watermark">
        <span>DEV-MIND SURVIVOR ARCHIVE // OREGON SECTOR 7</span>
      </div>
    </div>
  );
};

export default AuthPage;
