import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Typography, Button } from "@mui/material";
import HomeRoundedIcon from "@mui/icons-material/HomeRounded";
import PriorityHighRoundedIcon from "@mui/icons-material/PriorityHighRounded";
import { DarkModeContext } from "../context/DarkModeContext";

const NotFoundPage = () => {
  const navigate = useNavigate();
  const { isDarkMode } = useContext(DarkModeContext);

  const styles = getStyles(isDarkMode);

  return (
    <Box sx={styles.container}>
      {/* Soft brand glow behind the card */}
      <Box sx={styles.glow} aria-hidden />

      <Box sx={styles.card} className="fade-in">
        {/* Gradient alert badge with pulse effect */}
        <Box sx={styles.badge} className="pulse-animation">
          <PriorityHighRoundedIcon sx={styles.badgeIcon} />
        </Box>

        <Typography component="div" sx={styles.code}>
          404
        </Typography>

        <Typography component="h1" sx={styles.title}>
          Page Not Found
        </Typography>

        <Typography sx={styles.message}>
          Oops! The page you are looking for does not exist or has been moved.
        </Typography>

        <Button
          onClick={() => navigate("/")}
          startIcon={<HomeRoundedIcon />}
          sx={styles.button}
        >
          Go Back Home
        </Button>
      </Box>
    </Box>
  );
};

// Dynamically return styles based on dark mode, matching the global theme.
const getStyles = (isDark) => ({
  container: {
    position: "relative",
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    overflow: "hidden",
    px: 2,
    py: 8,
    fontFamily: "Poppins, sans-serif",
    background: isDark
      ? "radial-gradient(1200px 600px at 50% -10%, #2a2314 0%, #16120a 60%)"
      : "radial-gradient(1200px 600px at 50% -10%, #fef3c7 0%, #fdf8ec 60%)",
  },
  glow: {
    position: "absolute",
    top: "12%",
    width: { xs: 280, sm: 420 },
    height: { xs: 280, sm: 420 },
    borderRadius: "50%",
    background:
      "radial-gradient(circle, rgba(245,158,11,0.28) 0%, rgba(245,158,11,0) 70%)",
    filter: "blur(8px)",
    pointerEvents: "none",
  },
  card: {
    position: "relative",
    zIndex: 1,
    width: "100%",
    maxWidth: 480,
    textAlign: "center",
    px: { xs: 3, sm: 5 },
    py: { xs: 4, sm: 5 },
    borderRadius: "24px",
    background: isDark ? "var(--ms-glass-strong)" : "var(--ms-glass-strong)",
    border: isDark ? "1px solid #33291a" : "1px solid #f0e6d2",
    boxShadow: isDark
      ? "0 24px 60px rgba(0,0,0,0.55)"
      : "0 24px 60px rgba(245,158,11,0.18)",
    backdropFilter: "blur(6px)",
  },
  badge: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    width: { xs: 92, sm: 108 },
    height: { xs: 92, sm: 108 },
    mx: "auto",
    mb: 2,
    borderRadius: "50%",
    background:
      "linear-gradient(135deg, #f59e0b 0%, #fbbf24 50%, #f59e0b 100%)",
    border: isDark ? "5px solid rgba(255,255,255,0.06)" : "5px solid #ffffff",
    boxShadow: isDark
      ? "0 14px 34px rgba(245,158,11,0.45)"
      : "0 14px 34px rgba(245,158,11,0.40)",
    animation: "pulse 1.5s infinite",
  },
  badgeIcon: {
    color: "#fff",
    fontSize: { xs: 50, sm: 60 },
  },
  code: {
    fontFamily: "Poppins, sans-serif",
    fontWeight: 800,
    lineHeight: 1,
    fontSize: { xs: 64, sm: 84 },
    letterSpacing: "-2px",
    background:
      "linear-gradient(135deg, #f59e0b 0%, #fbbf24 50%, #f59e0b 100%)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    backgroundClip: "text",
  },
  title: {
    fontFamily: "Poppins, sans-serif",
    fontWeight: 700,
    fontSize: { xs: 22, sm: 26 },
    color: isDark ? "#f6f6f8" : "#1a1a1a",
    mt: 1,
    mb: 1,
  },
  message: {
    fontFamily: "Poppins, sans-serif",
    fontSize: { xs: 14, sm: 15 },
    color: isDark ? "#c3b69c" : "#6e6250",
    maxWidth: 360,
    mx: "auto",
    mb: 3,
  },
  button: {
    fontFamily: "Poppins, sans-serif",
    fontWeight: 700,
    textTransform: "none",
    color: "#fff",
    px: 3,
    py: 1.1,
    borderRadius: "999px",
    background: "linear-gradient(135deg, #f59e0b 0%, #f59e0b 100%)",
    boxShadow: "0 10px 22px rgba(245,158,11,0.35)",
    transition: "transform 0.2s ease, box-shadow 0.2s ease",
    "&:hover": {
      background: "linear-gradient(135deg, #fbbf24 0%, #fcd34d 100%)",
      boxShadow: "0 14px 28px rgba(245,158,11,0.45)",
      transform: "translateY(-2px)",
    },
  },
});

export default NotFoundPage;
