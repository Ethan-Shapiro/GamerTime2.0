import React from "react";
import AppBar from "@mui/material/AppBar";
import Typography from "@mui/material/Typography";
import Toolbar from "@mui/material/Toolbar";
import Button from "@mui/material/Button";
import { Box } from "@mui/system";
import LoginOverlay from "./LoginButton";

const Navbar = ({ navbarLabel, addMessage }) => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography
            align="left"
            variant="h6"
            component="div"
            sx={{ flexGrow: 1 }}
          >
            {navbarLabel}
          </Typography>
          <LoginOverlay addMessage={addMessage}></LoginOverlay>
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default Navbar;
