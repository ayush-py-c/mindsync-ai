import React from "react";
import { Box, IconButton, Tooltip, Typography } from "@mui/material";
import HomeIcon from "@mui/icons-material/Home";
import ExploreIcon from "@mui/icons-material/Explore";
import QueueMusicIcon from "@mui/icons-material/QueueMusic";
import PersonIcon from "@mui/icons-material/Person";
import { useNavigate, useLocation } from "react-router-dom";

// Floating frosted-glass dock -- the primary navigation for the signed-in
// app. Replaces the old tab row in the navbar on every viewport. Routes are
// already gated by RequireAuth, so a tap while signed out simply lands on
// /login, same as the old drawer behaviour.
const DOCK_ITEMS = [
  { label: "Home", path: "/home", icon: HomeIcon },
  { label: "Explore", resultsLabel: "Results", path: "/results", icon: ExploreIcon },
  { label: "For You", path: "/recommendations", icon: QueueMusicIcon },
  { label: "Profile", path: "/profile", icon: PersonIcon },
];

const BottomDock = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // /results reads as "Explore" until the user actually arrives from an
  // analysis (state carries the detected emotion) -- mirrors the navbar.
  const arrivedFromAnalysis =
    location.pathname === "/results" &&
    Boolean(location.state && location.state.emotion);

  return (
    <Box
      component="nav"
      aria-label="Primary"
      className="ms-glass"
      sx={{
        position: "fixed",
        left: "50%",
        bottom: { xs: 10, sm: 18 },
        transform: "translateX(-50%)",
        zIndex: 1200,
        display: "flex",
        alignItems: "center",
        gap: { xs: 2, sm: 3 },
        px: { xs: 1.5, sm: 2 },
        py: 0.75,
        borderRadius: "999px",
        maxWidth: "calc(100vw - 24px)",
        paddingBottom: {
          xs: "calc(6px + env(safe-area-inset-bottom, 0px))",
          sm: "6px",
        },
      }}
    >
      {DOCK_ITEMS.map((item) => {
        const Icon = item.icon;
        const active = location.pathname === item.path;
        const label =
          item.path === "/results" && arrivedFromAnalysis && item.resultsLabel
            ? item.resultsLabel
            : item.label;
        return (
          <Tooltip key={item.path} title={label} placement="top">
            <IconButton
              onClick={() => navigate(item.path)}
              aria-label={label}
              aria-current={active ? "page" : undefined}
              sx={{
                display: "flex",
                flexDirection: "row",
                gap: 0.75,
                px: { xs: 1.25, sm: 1.75 },
                py: 0.75,
                borderRadius: "999px",
                color: active ? "var(--ms-accent)" : "var(--ms-text-soft)",
                background: active
                  ? "rgba(251, 191, 36, 0.18)"
                  : "transparent",
                transition: "all .2s ease",
                "&:hover": {
                  background: active
                    ? "rgba(251, 191, 36, 0.22)"
                    : "rgba(251, 191, 36, 0.1)",
                  color: active ? "var(--ms-accent)" : "var(--ms-text)",
                },
              }}
            >
              <Icon sx={{ fontSize: 22 }} />
              <Typography
                sx={{
                  display: { xs: "none", sm: "inline" },
                  fontFamily: "Poppins",
                  fontWeight: active ? 700 : 600,
                  fontSize: 13,
                  color: "inherit",
                }}
              >
                {label}
              </Typography>
            </IconButton>
          </Tooltip>
        );
      })}
    </Box>
  );
};

export default BottomDock;
