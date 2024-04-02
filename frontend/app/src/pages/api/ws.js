const WS_URL = `ws://${process.env.NEXT_PUBLIC_API_HOST}:${process.env.NEXT_PUBLIC_API_PORT}/ws`;

export { WS_URL };

export const getWsRoomUrl = (roomId) => `${WS_URL}/room/${roomId}/`;
