import Plyr from 'plyr-react'
import 'plyr-react/plyr.css'

type ComponentProps = {
  video_url: string
  thumbnail_url: string
}

const VideoPlayer: React.FC<ComponentProps> = ({ video_url, thumbnail_url }) => {
  return (
    <div className='relative aspect-[16/9] rounded-2xl overflow-hidden'>
      <Plyr
        source={{
          type: 'video',
          sources: [
            {
              src: video_url,
              type: 'video/mp4',
            },
          ],
          poster: thumbnail_url,
        }}
        options={{
          blankVideo: 'blank.mp4',
          autopause: true,
          hideControls: false,
          controls: ['play', 'progress', 'current-time', 'fullscreen'],
          ratio: '16:9',
        }}
      />
    </div>
  )
}

export default VideoPlayer
