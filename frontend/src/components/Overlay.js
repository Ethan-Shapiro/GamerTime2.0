import React from "react";
import { Backdrop, Box, Button } from "@mui/material";

const Overlay = ({ open, setOpen, setOverlayResponse }) => {
  const handleClose = () => {
    setOpen(false);
  };
  const handleToggle = () => {
    setOpen(!open);
  };
  return (
    <Backdrop
      sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
      open={open}
      onClick={handleClose}
    >
      <Box
        component="form"
        sx={{
          "& > :not(style)": { m: 1, width: "25ch" },
        }}
        noValidate
        autoComplete="off"
      >
        <Box sx={{ border: 1, borderRadius: 5 }}>
          <p>Start Computer Session?</p>
          <Button
            variant="contained"
            onClick={() => {
              setOverlayResponse(true);
            }}
          >
            Start
          </Button>
          <Button
            variant="contained"
            sx={{ backgroundColor: "#616161" }}
            onClick={() => {
              setOverlayResponse(false);
            }}
          >
            Cancel
          </Button>
        </Box>
      </Box>
    </Backdrop>
  );
};

export default Overlay;
