import React, { useEffect, useState } from "react";
import {
  Backdrop,
  Box,
  Button,
  Typography,
  Grid,
  TextField,
  FormControl,
  InputLabel,
  InputAdornment,
  IconButton,
} from "@mui/material";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import OutlinedInput from "@mui/material/OutlinedInput";
import axios from "axios";

const LoginOverlay = () => {
  const [loggedIn, setLoginStatus] = useState(false);
  const [open, setOpen] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  // Check if token is present and display login or sign out accordingly
  useEffect(() => {
    if (localStorage.getItem("jwt") !== null) {
      setLoginStatus(true);
    }
  }, []);

  const handleClick = () => {
    if (loggedIn) {
      attemptSignOut();
    } else {
      setOpen(true);
    }
  };

  const attemptSignOut = () => {
    localStorage.removeItem("jwt");
    setLoginStatus(false);
  };

  const attemptLogin = () => {
    console.log("Attempting to login!");
    console.log(email);
    console.log(password);
    axios
      .post("/api/auth/login", {
        email: email,
        password: password,
      })
      .then((response) => {
        console.log(response);
        if (response.data["success"]) {
          const accessToken = response.data["access_token"];
          localStorage.setItem("jwt", accessToken);
          setLoginStatus(true);
        } else {
          // say incorrect login or something
          setLoginStatus(false);
        }
      })
      .catch((error) => {
        console.log(error.response);
      });
    handleClose();
  };

  const handleClose = () => {
    setOpen(false);
    setEmail("");
    setPassword("");
  };

  return (
    <div>
      <Button onClick={handleClick} color="inherit">
        {loggedIn ? "Sign Out" : "Login"}
      </Button>
      <Backdrop
        sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={open}
      >
        <Box
          component="form"
          sx={{
            "& > :not(style)": { m: 1, width: "50ch" },
          }}
          noValidate
          autoComplete="off"
        >
          <Box sx={{ border: 1, borderRadius: 5 }}>
            <Typography variant="h4">Login</Typography>
            <Grid container>
              <Grid xs={6}>
                <TextField
                  required
                  id="firstname-input"
                  label="Email"
                  variant="outlined"
                  value={email}
                  onChange={(event) => {
                    setEmail(event.target.value);
                  }}
                />
              </Grid>
              <Grid xs={6}>
                <FormControl variant="outlined">
                  <InputLabel htmlFor="outlined-adornment-password">
                    Password
                  </InputLabel>
                  <OutlinedInput
                    id="outlined-adornment-password"
                    required
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(event) => {
                      setPassword(event.target.value);
                    }}
                    endAdornment={
                      <InputAdornment position="end">
                        <IconButton
                          aria-label="toggle password visibility"
                          onClick={() => {
                            setShowPassword(!showPassword);
                          }}
                          onMouseDown={(event) => {
                            event.preventDefault();
                          }}
                          edge="end"
                        >
                          {showPassword ? <VisibilityOff /> : <Visibility />}
                        </IconButton>
                      </InputAdornment>
                    }
                    label="Password"
                  />
                </FormControl>
              </Grid>
            </Grid>
            <Button variant="contained" onClick={attemptLogin}>
              Login
            </Button>
            <Button
              variant="contained"
              sx={{ backgroundColor: "#616161" }}
              onClick={handleClose}
            >
              Cancel
            </Button>
          </Box>
        </Box>
      </Backdrop>
    </div>
  );
};

export default LoginOverlay;
