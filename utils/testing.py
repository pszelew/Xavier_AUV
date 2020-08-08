import cv2

def frame_preview(camera_client, exit_key='q'):
    """
    Get frame preview
    :param camera_client: [CameraClient] connected camera client to get frame
    :param exit_key: [Char] Key to exit preview
    :return:
    """
    while True:
        cv2.imshow(f'Press {exit_key} to exit', camera_client.frame)
        if cv2.waitKey(1) & 0xFF == ord(exit_key):
            cv2.destroyAllWindows()
            break