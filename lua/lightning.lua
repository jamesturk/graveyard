NUM_CIRCLES = 20
NEW_CIRCLE = 0.05

function new_circle()
    return {
        x = math.random(-100, 800),
        y = math.random(-100, 600), 
        r = math.random(10, 100),
        hoffset = math.random(-50, 20),
        saturation = math.random(28, 100), 
        lightness = math.random(128, 200),
        alpha = math.random(128, 255)
    }
end


function hsl(h, s, l, a)
    if s<=0 then return l,l,l,a end
    h, s, l = h/256*6, s/255, l/255
    local c = (1-math.abs(2*l-1))*s
    local x = (1-math.abs(h%2-1))*c
    local m,r,g,b = (l-.5*c), 0,0,0
    if h < 1     then r,g,b = c,x,0
    elseif h < 2 then r,g,b = x,c,0
    elseif h < 3 then r,g,b = 0,c,x
    elseif h < 4 then r,g,b = 0,x,c
    elseif h < 5 then r,g,b = x,0,c
    else              r,g,b = c,0,x
    end return (r+m)*255,(g+m)*255,(b+m)*255,a
end

function love.load()
    s = 3
    clock = 0
    direction = 10
    hue = 70
    circles = {}
    for i = 1, NUM_CIRCLES, 1 do
        table.insert(circles, new_circle())
    end
end
 
function love.update(dt)
    -- if s > 10 then
    --     direction = -10
    -- elseif s < 3.3 then
    --     direction = 10
    -- end

    -- s = s + (direction*dt)

    hue = (hue + 15*dt)
    if hue > 255 then hue = 0 end
    print(hue)

    clock = clock + dt
    if clock > NEW_CIRCLE then 
        clock = clock - NEW_CIRCLE
        circles[math.random(1, 10)] = new_circle()
    end
end

function love.keypressed(key, scancode, isrepeat)
    if scancode == 'right' then
        s = s + 1
    elseif scancode == 'left' then
        s = s - 1
    end
end
 

function love.draw()
    for i, circle in pairs(circles) do
        love.graphics.setColor(hsl(hue + circle.hoffset, circle.saturation, circle.lightness, circle.alpha))
        love.graphics.ellipse('fill', circle.x, circle.y, circle.r, circle.r, s)
    end
end
