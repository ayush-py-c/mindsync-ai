import { createTheme } from "@mui/material/styles";

// MindSync AI design language -- warm amber/gold accent on frosted-glass
// surfaces. Poppins is forced on every MUI component so nothing falls back
// to Roboto and fights the body CSS.
const POPPINS = '"Poppins", "Helvetica Neue", Arial, sans-serif';

const theme = createTheme({
  palette: {
    primary: { main: "#d97706", contrastText: "#221b10" },
    secondary: { main: "#fbbf24", contrastText: "#221b10" },
    background: { default: "#fdf8ec", paper: "#ffffff" },
    text: { primary: "#241d11", secondary: "#6e6250" },
  },
  shape: { borderRadius: 16 },
  typography: {
    fontFamily: POPPINS,
    h1: { fontFamily: POPPINS },
    h2: { fontFamily: POPPINS },
    h3: { fontFamily: POPPINS },
    h4: { fontFamily: POPPINS, fontWeight: 600 },
    h5: { fontFamily: POPPINS },
    h6: { fontFamily: POPPINS },
    subtitle1: { fontFamily: POPPINS },
    subtitle2: { fontFamily: POPPINS },
    body1: { fontFamily: POPPINS },
    body2: { fontFamily: POPPINS },
    button: { fontFamily: POPPINS, textTransform: "none" },
    caption: { fontFamily: POPPINS },
    overline: { fontFamily: POPPINS },
  },
  components: {
    // Every Paper (Card, Dialog, Menu, Drawer, ...) becomes frosted glass.
    // The concrete tint is applied per-mode from styles.css so the same
    // rule works in light and dark without a JS-driven theme swap; here we
    // just neutralise MUI's opaque defaults so the CSS can win.
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
          backgroundColor: "transparent",
        },
      },
    },
    MuiCssBaseline: {
      styleOverrides: {
        body: { fontFamily: POPPINS },
        input: {
          fontFamily: POPPINS,
          WebkitAppearance: "none",
          appearance: "none",
        },
        textarea: { fontFamily: POPPINS },
        button: { fontFamily: POPPINS },
        select: {
          fontFamily: POPPINS,
          WebkitAppearance: "none",
          appearance: "none",
        },
        // Defeat Chrome / Edge autofill background tint globally.
        "input:-webkit-autofill, input:-webkit-autofill:hover, input:-webkit-autofill:focus, input:-webkit-autofill:active":
          {
            WebkitBoxShadow: "0 0 0 1000px transparent inset",
            WebkitTextFillColor: "currentColor",
            caretColor: "currentColor",
            transition: "background-color 5000s ease-in-out 0s",
            backgroundColor: "transparent !important",
            backgroundImage: "none !important",
          },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          fontFamily: POPPINS,
          fontWeight: 700,
          borderRadius: "999px",
        },
        contained: {
          backgroundImage:
            "linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%)",
          color: "#221b10",
          boxShadow: "0 6px 18px rgba(180, 83, 9, 0.22)",
          "&:hover": {
            backgroundImage:
              "linear-gradient(135deg, #fcd34d 0%, #f59e0b 100%)",
            boxShadow: "0 8px 22px rgba(180, 83, 9, 0.3)",
          },
        },
        outlined: {
          borderColor: "rgba(180, 83, 9, 0.35)",
          color: "#b45309",
          "&:hover": {
            borderColor: "#b45309",
            backgroundColor: "rgba(251, 191, 36, 0.12)",
          },
        },
        text: {
          "&:hover": { backgroundColor: "rgba(251, 191, 36, 0.14)" },
        },
      },
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          "&:hover": { backgroundColor: "rgba(251, 191, 36, 0.14)" },
        },
      },
    },
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          backgroundColor: "transparent",
          borderRadius: 14,
          "& .MuiOutlinedInput-notchedOutline": {
            borderColor: "rgba(146, 64, 14, 0.22)",
          },
          "&:hover .MuiOutlinedInput-notchedOutline": {
            borderColor: "rgba(217, 119, 6, 0.5)",
          },
          "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
            borderColor: "#d97706",
            borderWidth: 1.5,
          },
        },
      },
    },
    MuiInputBase: {
      styleOverrides: {
        root: { fontFamily: POPPINS, backgroundColor: "transparent" },
        input: {
          backgroundColor: "transparent",
          WebkitAppearance: "none",
          appearance: "none",
          boxShadow: "none",
        },
      },
    },
    MuiInputLabel: { styleOverrides: { root: { fontFamily: POPPINS } } },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          fontFamily: POPPINS,
          borderRadius: 10,
          marginInline: 8,
          "&:hover": { backgroundColor: "rgba(251, 191, 36, 0.14)" },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          fontFamily: POPPINS,
          borderRadius: 999,
          backgroundColor: "rgba(251, 191, 36, 0.16)",
          color: "#92400e",
        },
      },
    },
    MuiTab: { styleOverrides: { root: { fontFamily: POPPINS } } },
    MuiTooltip: { styleOverrides: { tooltip: { fontFamily: POPPINS } } },
    MuiSwitch: {
      styleOverrides: {
        root: {
          "& .MuiSwitch-switchBase.Mui-checked": { color: "#f59e0b" },
          "& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track": {
            backgroundColor: "#f59e0b",
          },
        },
      },
    },
  },
});

export default theme;
