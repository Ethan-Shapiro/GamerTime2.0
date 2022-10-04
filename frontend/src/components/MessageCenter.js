import React from "react";
import { Alert, Stack, Box, Backdrop } from "@mui/material";

const MessageCenter = ({ messages, removeMessage }) => {
  return (
    <Stack
      sx={{
        left: 0,
        position: "absolute",
        zIndex: 1,
        right: "60%",
        minWidth: 300,
        height: 0,
        maxWidth: 500,
      }}
      direction="column"
      spacing={2}
    >
      {messages.map((item, index) => {
        return (
          <Alert
            key={index}
            variant="filled"
            severity={item["messageType"]}
            onClose={() => removeMessage(index)}
          >
            {item["message"]}
          </Alert>
        );
      })}
    </Stack>
  );
};

export default MessageCenter;
