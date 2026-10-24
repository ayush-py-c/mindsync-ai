import {
  Box,
  Button,
  Card,
  CardContent,
  Paper,
  Typography,
} from "@mui/material";

const Recommendations = ({ recommendations }) => {
  return (
    <Paper elevation={4} style={styles.resultsContainer}>
      <Typography
        variant="h6"
        style={{ fontFamily: "Poppins", marginBottom: "10px" }}
      >
        Your Recommendations
      </Typography>
      <Box sx={styles.recommendationsList}>
        {recommendations.length > 0 ? (
          recommendations.map((rec, index) => (
            <Card key={index} sx={styles.recommendationCard}>
              <Box sx={styles.cardContentContainer}>
                {/* Left Half: Image */}
                <Box sx={styles.imageContainer}>
                  <img
                    src={rec.image_url}
                    alt={`${rec.name} album cover`}
                    style={styles.albumImage}
                  />
                </Box>

                {/* Right Half: Song Details */}
                  <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                    <Typography variant="subtitle1" style={styles.songTitle}>
                      {rec.name}
                    </Typography>
                    {rec.language === "hindi" && (
                      <span
                        style={{
                          fontSize: "10px",
                          fontWeight: 700,
                          padding: "2px 6px",
                          borderRadius: "4px",
                          background: "rgba(245, 158, 11, 0.2)",
                          color: "#f59e0b",
                          border: "1px solid rgba(245, 158, 11, 0.4)",
                        }}
                      >
                        Hindi 🇮🇳
                      </span>
                    )}
                  </Box>
                  <Typography variant="body2" style={styles.artistName}>
                    {rec.artist}
                  </Typography>
                  {rec.preview_url && (
                    <audio controls style={styles.audioPlayer}>
                      <source src={rec.preview_url} type="audio/mpeg" />
                      Your browser does not support the audio element.
                    </audio>
                  )}
                  <Button
                    href={rec.external_url}
                    target="_blank"
                    variant="contained"
                    color="primary"
                    style={styles.playerButton}
                  >
                    Listen on Deezer
                  </Button>
                </CardContent>
              </Box>
            </Card>
          ))
        ) : (
          <Typography
            variant="body2"
            style={{
              color: "#999",
              marginTop: "20px",
              textAlign: "center",
              font: "inherit",
              fontSize: "14px",
            }}
          >
            No recommendations available. Try inputting a new image, changing
            the mood, entering some texts, or recording something...
          </Typography>
        )}
      </Box>
    </Paper>
  );
};

export default Recommendations;
