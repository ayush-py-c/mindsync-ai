import React, { useEffect, useState, useContext } from "react";
import {
  AppBar,
  Box,
  Button,
  Divider,
  IconButton,
  Menu,
  MenuItem,
  Toolbar,
  Tooltip,
  Typography,
} from "@mui/material";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import LightModeIcon from "@mui/icons-material/LightMode";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import LoginIcon from "@mui/icons-material/Login";
import LogoutIcon from "@mui/icons-material/Logout";
import MusicNoteIcon from "@mui/icons-material/MusicNote";
import FingerprintIcon from "@mui/icons-material/Fingerprint";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import { useNavigate, useLocation } from "react-router-dom";

import { DarkModeContext } from "../context/DarkModeContext";
import { isAuthenticated, logout, AUTH_EVENT } from "../services/auth";

// Slim frosted-glass top bar. Primary navigation lives in the bottom dock;
// the bar keeps the brand, theme toggle and the account menu.
const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [isLoggedIn, setIsLoggedIn] = useState(isAuthenticated());
  const [accountAnchor, setAccountAnchor] = useState(null);

  const { isDarkMode, toggleDarkMode } = useContext(DarkModeContext);

  // Token validity is determined by decoding the JWT locally (no network,
  // no polling). The navbar re-syncs on route changes and on auth-change
  // events -- login/logout/refresh in this tab, or token changes in
  // another tab (via the storage event).
  useEffect(() => {
    const sync = () => setIsLoggedIn(isAuthenticated());
    sync();
    window.addEventListener(AUTH_EVENT, sync);
    window.addEventListener("storage", sync);
    return () => {
      window.removeEventListener(AUTH_EVENT, sync);
      window.removeEventListener("storage", sync);
    };
  }, [location]);

  const handleLogout = () => {
    // Close the menu first, then redirect with replace so there's a single
    // history entry and no duplicate navigation.
    setAccountAnchor(null);
    logout();
    setIsLoggedIn(false);
    navigate("/login", { replace: true });
  };

  const goto = (path) => {
    setAccountAnchor(null);
    navigate(path);
  };

  return (
    <AppBar
      position="sticky"
      elevation={0}
      sx={{
        background: "var(--ms-glass-strong)",
        color: "var(--ms-text)",
        backdropFilter: "var(--ms-blur)",
        WebkitBackdropFilter: "var(--ms-blur)",
        borderBottom: "1px solid var(--ms-glass-border)",
        transition: "background 0.3s ease",
      }}
    >
      <Toolbar
        sx={{
          maxWidth: 1280,
          mx: "auto",
          width: "100%",
          gap: 2,
          py: 0.6,
        }}
      >
        {/* ---- Brand ---- */}
        <Box
          onClick={() => navigate(isLoggedIn ? "/home" : "/")}
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 1.25,
            cursor: "pointer",
            mr: "auto",
            "&:hover .brand-mark": { transform: "rotate(-6deg) scale(1.04)" },
          }}
        >
          <Box
            className="brand-mark"
            sx={{
              width: 36,
              height: 36,
              borderRadius: "12px",
              background: "var(--ms-accent-gradient)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: "0 6px 16px rgba(180, 83, 9, 0.32)",
              transition: "transform .3s cubic-bezier(.34,1.56,.64,1)",
            }}
          >
            <MusicNoteIcon sx={{ color: "#221b10", fontSize: 21 }} />
          </Box>
          <Typography
            sx={{
              fontFamily: "Poppins",
              fontWeight: 800,
              fontSize: { xs: 18, sm: 21 },
              letterSpacing: "-0.02em",
              color: "var(--ms-text)",
              whiteSpace: "nowrap",
            }}
          >
            MindSync{" "}
            <Box
              component="span"
              sx={{
                background: "var(--ms-accent-gradient)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
                backgroundClip: "text",
              }}
            >
              AI
            </Box>
          </Typography>
        </Box>

        {/* ---- Right cluster ---- */}
        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
          {isLoggedIn ? (
            <>
              <Button
                onClick={(e) => setAccountAnchor(e.currentTarget)}
                startIcon={<AccountCircleIcon sx={{ fontSize: 18 }} />}
                endIcon={
                  <KeyboardArrowDownIcon
                    sx={{
                      fontSize: 18,
                      transition: "transform .2s ease",
                      transform: accountAnchor
                        ? "rotate(180deg)"
                        : "rotate(0deg)",
                    }}
                  />
                }
                aria-haspopup="true"
                aria-expanded={Boolean(accountAnchor)}
                sx={{
                  color: "var(--ms-text)",
                  fontWeight: 700,
                  fontSize: 14,
                  borderRadius: "999px",
                  textTransform: "none",
                  px: 2,
                  py: 0.85,
                  border: "1px solid var(--ms-glass-border)",
                  background: accountAnchor
                    ? "rgba(251,191,36,0.14)"
                    : "transparent",
                  "&:hover": { background: "rgba(251,191,36,0.14)" },
                }}
              >
                Account
              </Button>
              <Menu
                anchorEl={accountAnchor}
                open={Boolean(accountAnchor)}
                onClose={() => setAccountAnchor(null)}
                anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
                transformOrigin={{ vertical: "top", horizontal: "right" }}
                slotProps={{
                  paper: {
                    sx: {
                      mt: 1,
                      minWidth: 200,
                      borderRadius: "16px",
                      overflow: "hidden",
                    },
                  },
                }}
              >
                <MenuItem
                  onClick={() => goto("/passkeys")}
                  sx={{
                    fontWeight: 600,
                    fontSize: 14,
                    py: 1.25,
                    color: "var(--ms-text)",
                    "&:hover": { background: "rgba(251,191,36,0.14)" },
                  }}
                >
                  <ListItemIconOnly>
                    <FingerprintIcon fontSize="small" />
                  </ListItemIconOnly>
                  Passkeys
                </MenuItem>
                <Divider sx={{ my: 0.5 }} />
                <MenuItem
                  onClick={handleLogout}
                  sx={{
                    fontWeight: 700,
                    fontSize: 14,
                    py: 1.25,
                    color: "var(--ms-accent)",
                    "&:hover": { background: "rgba(251,191,36,0.16)" },
                  }}
                >
                  <ListItemIconOnly>
                    <LogoutIcon fontSize="small" />
                  </ListItemIconOnly>
                  Log Out
                </MenuItem>
              </Menu>
            </>
          ) : (
            <Button
              onClick={() => navigate("/login")}
              startIcon={<LoginIcon sx={{ fontSize: 18 }} />}
              sx={{
                color: "#221b10",
                fontWeight: 700,
                fontSize: 14,
                borderRadius: "999px",
                textTransform: "none",
                px: 2.5,
                py: 0.85,
                background: "var(--ms-accent-gradient)",
                boxShadow: "0 8px 18px rgba(180, 83, 9, 0.28)",
                "&:hover": {
                  background: "var(--ms-accent-gradient)",
                  filter: "brightness(1.05)",
                  transform: "translateY(-1px)",
                },
              }}
            >
              Sign in
            </Button>
          )}

          <Tooltip title={isDarkMode ? "Switch to light" : "Switch to dark"}>
            <IconButton
              onClick={toggleDarkMode}
              aria-label="Toggle dark mode"
              sx={{
                color: "var(--ms-text)",
                border: "1px solid var(--ms-glass-border)",
                borderRadius: "12px",
                background: "rgba(251,191,36,0.08)",
                "&:hover": { background: "rgba(251,191,36,0.16)" },
              }}
            >
              {isDarkMode ? <LightModeIcon /> : <DarkModeIcon />}
            </IconButton>
          </Tooltip>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

// Small inline wrapper: keeps menu icon alignment without pulling in the
// full MUIListItemIcon (which brings its own flex rules).
const ListItemIconOnly = ({ children }) => (
  <Box
    component="span"
    sx={{
      display: "inline-flex",
      minWidth: 24,
      mr: 1,
      color: "inherit",
      alignItems: "center",
    }}
  >
    {children}
  </Box>
);

export default Navbar;
